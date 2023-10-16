from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QToolBar,
    QApplication,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QDialogButtonBox,
    QFormLayout,
    QDialog,
    QFileDialog,
    QInputDialog,
    QSizePolicy,
)

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import json
from datetime import date

from dataparser import Parser
from functools import reduce


class ActionBar(QToolBar):
    def __init__(self, parent_widget, data):
        super().__init__()
        self.data = data
        self.parent_widget = parent_widget

        self.add_entry = QAction("Add Entry")
        self.remove_entry = QAction("Remove Entry")
        # self.edit_entry = QAction("Edit Entry")
        self.import_data = QAction("Import Data")
        self.help = QAction("Help")

        self.add_entry.triggered.connect(self._on_add_entry_click)
        self.import_data.triggered.connect(self._on_import_data_click)
        self.remove_entry.triggered.connect(self._on_remove_entry_click)
        self.addAction(self.add_entry)
        self.addAction(self.remove_entry)
        # self.addAction(self.edit_entry)
        self.addAction(self.import_data)
        self.addAction(self.help)

    def _on_add_entry_click(self):
        dialog = AddEntry(self.data, self.parent_widget.table.refresh_data)
        dialog.exec()

    def _on_remove_entry_click(self):
        date, ok = QInputDialog.getText(self, "Remove an Entry", "Date to remove:", QLineEdit.Normal)
        if date and ok:
            Parser.remove(date)

        self.parent_widget.table.refresh_data()

    def _on_import_data_click(self):
        delimiter = " "
        file_name = QFileDialog.getOpenFileName(
            self, "Choose Data Source", "/", "Data Files (*.csv, *.txt)"
        )


class AddEntry(QDialog):
    def __init__(self, data, refresh_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.data = data
        self.setWindowTitle("Add Entry")

        self.nrows = len(self.data["exercises"]) + 3
        self.ncols = 4
        self.nsets = 1
        self.form = QTableWidget()

        self._init_form()
        self.form.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)

        save_button = QDialogButtonBox.StandardButton.Save
        self.add_exercise_button = QPushButton("Add New Exercise")
        self.add_sets_button = QPushButton("Add Sets")

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(save_button)
        self.buttonBox.addButton(self.add_exercise_button, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.add_sets_button, QDialogButtonBox.ButtonRole.ActionRole)

        self.buttonBox.accepted.connect(self.ok)
        self.add_exercise_button.released.connect(self.add_exercise)
        self.add_sets_button.released.connect(self.add_sets)
        # self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.form)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def ok(self):
        date = self.form.item(self.nrows - 1, 1).text()

        # edit the data
        for row_idx in range(1, self.nrows - 2):
            name = self.form.item(row_idx, 0).text()

            # build entry for exercise
            entry = {}
            setn_update = 0
            for setn, col_idx in enumerate(range(1, 1 + 2 * self.nsets, 2), start=1):
                if (
                    (weight := self.form.item(row_idx, col_idx))
                    and (reps := self.form.item(row_idx, col_idx + 1))
                    and (w := weight.text())
                    and (r := reps.text())
                ):
                    setn_update = setn
                    entry[f"set{setn}"] = {"weight": w, "reps": r}

            if setn_update:
                entry["nsets"] = setn_update
                entry["notes"] = (
                    self.form.item(row_idx, col_idx + 2).text()
                    if self.form.item(row_idx, col_idx + 2)
                    else ""
                )

                # update data
                Parser.add(entry, name, date, row_idx - 1)

        #print(self.data)
        self.refresh_callback()

        self.accept()

    def add_exercise(self):
        ex_name, ok = QInputDialog.getText(self, "Enter New Exercise", "Name:", QLineEdit.Normal)
        if ex_name and ok:
            self.form.insertRow(self.nrows - 2)
            self.form.setItem(self.nrows - 2, 0, QTableWidgetItem(ex_name))
            self.nrows += 1

        self.adjustSize()

    def add_sets(self):
        nsets, ok = QInputDialog.getInt(
            self,
            "Enter Number of Sets to Add",
            "Number of Sets to Add:",
        )
        if nsets and ok:
            for n in range(nsets):
                self.form.insertColumn(self.ncols - 1 + 2 * n)
                self.form.insertColumn(self.ncols - 0 + 2 * n)

                self.form.setItem(
                    0,
                    self.ncols - 1 + 2 * n,
                    QTableWidgetItem(f"Set {n+1+self.nsets} Weight"),
                )
                self.form.setItem(
                    0,
                    self.ncols - 0 + 2 * n,
                    QTableWidgetItem(f"Set {n+1+self.nsets} Reps"),
                )

            self.ncols += 2 * nsets
            self.nsets += nsets

        self.adjustSize()

    def _init_form(self):
        self.form.setRowCount(self.nrows)
        self.form.setColumnCount(self.ncols)

        # set headers
        self.form.setItem(0, 1, QTableWidgetItem(f"Set 1 Weight"))
        self.form.setItem(0, 2, QTableWidgetItem(f"Set 1 Reps"))
        self.form.setItem(0, 3, QTableWidgetItem(f"Notes"))

        for row_index, ex in enumerate(self.data["exercises"], start=1):
            self.form.setItem(row_index, 0, QTableWidgetItem(ex["name"]))

        self.form.setItem(self.nrows - 1, 0, QTableWidgetItem("Date"))
        self.form.setItem(self.nrows - 1, 1, QTableWidgetItem(date.today().isoformat()))


