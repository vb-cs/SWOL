from PySide6.QtWidgets import (
    QWidget,
    QLabel,
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
)

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import json
from datetime import date

from dataparser import Parser
from functools import reduce


class ActionBar(QToolBar):
    def __init__(self, parent, data):
        super().__init__()
        self.data = data
        self.parent = parent

        self.add_entry = QAction("Add Entry")
        self.remove_entry = QAction("Remove Entry")
        # self.edit_entry = QAction("Edit Entry")
        self.import_data = QAction("Import Data")
        self.help = QAction("Help")

        self.add_entry.triggered.connect(self._on_add_entry_click)

        self.addAction(self.add_entry)
        self.addAction(self.remove_entry)
        # self.addAction(self.edit_entry)
        self.addAction(self.import_data)
        self.addAction(self.help)

    def _on_add_entry_click(self):
        dialog = AddEntry(self.data, self.parent.table.refresh_data)
        dialog.exec()


class AddEntry(QDialog):
    def __init__(self, data, refresh_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.data = data
        self.set_count = 1
        self.setWindowTitle("Add Entry")

        self.form = QTableWidget()
        self.build_form()

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.ok)
        # self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.form)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def ok(self):
        date = self.form.item(self.nrows - 1, 1).text()

        # edit the data
        for row_idx in range(1, self.nrows - 2):
            print(row_idx)
            name = self.form.item(row_idx, 0).text()

            # build entry for exercise
            entry = {}
            count = 0
            for col_idx in range(1, 1 + 2 * self.set_count, 2):
                if (weight := self.form.item(row_idx, col_idx)) and (
                    reps := self.form.item(row_idx, col_idx + 1)
                ):
                    count += 1
                    entry[f"set{count}"] = {
                        "weight": weight.text(),
                        "reps": reps.text(),
                    }

            if count:
                entry["set_count"] = count
                print(col_idx)
                entry["notes"] = (
                    self.form.item(row_idx, col_idx + 2).text()
                    if self.form.item(row_idx, col_idx + 2)
                    else ""
                )
                print(entry)
                # update data
                self.data["exercises"][row_idx - 1]["data"][date] = entry

        self.refresh_callback()

        self.accept()

    def build_form(self):
        self.nrows = len(self.data["exercises"]) + 3
        self.ncol = 4
        self.form.setRowCount(self.nrows)
        self.form.setColumnCount(self.ncol)

        # set headers
        self.form.setItem(0, 1, QTableWidgetItem(f"Set 1 Weight"))
        self.form.setItem(0, 2, QTableWidgetItem(f"Set 1 Reps"))
        self.form.setItem(0, 3, QTableWidgetItem(f"Notes"))

        for row_index, ex in enumerate(self.data["exercises"], start=1):
            self.form.setItem(row_index, 0, QTableWidgetItem(ex["name"]))

        self.form.setItem(self.nrows - 1, 0, QTableWidgetItem("Date"))
        self.form.setItem(self.nrows - 1, 1, QTableWidgetItem(date.today().isoformat()))
