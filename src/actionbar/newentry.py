from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QToolBar,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QDialogButtonBox,
    QFormLayout,
    QDialog,
    QFileDialog,
    QInputDialog,
    QSizePolicy,
    QHBoxLayout,
    QComboBox,
    QStyle,
    QApplication,
    QListWidget
)

from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from datetime import date

from ..model.model import Data
from functools import reduce
from pathlib import Path


class ExerciseEntry(QWidget):
    def __init__(self, exercise=""):
        super().__init__()

        self.mainLayout = QHBoxLayout()
        self.exerciseEdit = QLineEdit(exercise)
        self.weightEdits = [QLineEdit()]
        self.repsEdits = [QLineEdit()]
        self.notes = QLineEdit()
        self.system = QComboBox()
        self.system.addItems(["kg", "lbs"])
        self.system.setEditable(False)
        self.upButton = QPushButton("Move Up")
        self.downButton = QPushButton("Move Down")
        # self.upButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
        # self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
        # self.downButton.setIcon(QIcon.fromTheme("go_up"))
        # self.downButton.setIcon(QStyle.standardIcon(QStyle.SP_DirClosedIcon))

        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.addWidget(self.upButton)
        self.buttonLayout.addWidget(self.downButton)

        self.mainLayout.addWidget(self.exerciseEdit)
        for weightEdit, repsEdit in zip(self.weightEdits, self.repsEdits):
            self.mainLayout.addWidget(weightEdit)
            self.mainLayout.addWidget(repsEdit)
        self.mainLayout.addWidget(self.notes)
        self.mainLayout.addWidget(self.system)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setLayout(self.mainLayout)

    def add_set_column(self):
        weightEdit = QLineEdit()
        repsEdit = QLineEdit()

        self.mainLayout.insertWidget(1 + 2 * len(self.weightEdits), weightEdit)
        self.mainLayout.insertWidget(2 + 2 * len(self.weightEdits), repsEdit)

        self.weightEdits.append(QLineEdit())
        self.repsEdits.append(QLineEdit())


class NewEntry(QDialog):
    def __init__(self, data, refresh_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.data = data
        self.setWindowTitle("New Entry")

        self.nrows = len(self.data["exercises"]) + 3
        self.ncols = 4
        self.nsets = 1

        self.header = QHBoxLayout()
        self.header.addWidget(QLabel("Exercise"))
        self.header.addWidget(QLabel("Set 1 Weight"))
        self.header.addWidget(QLabel("Set 1 Reps"))
        self.header.addWidget(QLabel("Notes"))

        self.exercise_entries = []
        self.form = QListWidget()
        self._init_form()

        self.dateEdit = QLineEdit()
        self.footer = QHBoxLayout()
        self.footer.addWidget(QLabel("Date"))
        self.footer.addWidget(self.dateEdit)

        self.form.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)

        save_button = QDialogButtonBox.StandardButton.Save
        cancel_button = QDialogButtonBox.StandardButton.Cancel
        self.new_exercise_button = QPushButton("Add Row")
        self.nsets_button = QPushButton("Add Set Column")

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(save_button)
        self.buttonBox.addButton(cancel_button)
        self.buttonBox.addButton(self.new_exercise_button, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.nsets_button, QDialogButtonBox.ButtonRole.ActionRole)

        self.buttonBox.accepted.connect(self._save)
        self.new_exercise_button.released.connect(self._add_row)
        self.nsets_button.released.connect(self._add_set_column)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.form)
        self.mainLayout.addWidget(self.footer)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

    def _init_form(self):
        

        self.exercise_entries = [ExerciseEntry(ex) for ex in Data.exercises()]
        self.form.addItems(self.exercise_entries)


        
        '''
        self.form.setRowCount(self.nrows)
        self.form.setColumnCount(self.ncols)

        # set headers
        self.form.setItem(0, 0, QTableWidgetItem(f"Exercise"))
        self.form.setItem(0, 1, QTableWidgetItem(f"Set 1 Weight"))
        self.form.setItem(0, 2, QTableWidgetItem(f"Set 1 Reps"))
        self.form.setItem(0, 3, QTableWidgetItem(f"Notes"))

        for row_index, ex_name in enumerate(self.data["exercises"], start=1):
            self.form.setItem(row_index, 0, QTableWidgetItem(ex_name))

        self.form.setItem(self.nrows - 1, 0, QTableWidgetItem("Date"))
        self.form.setItem(self.nrows - 1, 1, QTableWidgetItem(date.today().isoformat()))
        '''
    def _save(self):
        #

        sets = [["OHP"]*2, 
                ["Set 1 Weight", "Set 1 Reps"]]

        dates = ["2024-1-7"]
        columns = pd.MultiIndex.from_arrays(sets)
        new_df = pd.DataFrame(np.random.randn(1, 2), index=dates, columns=columns)

        date = self.form.item(self.nrows - 1, 1).text()

        # edit the data
        for row_idx in range(1, self.nrows - 2):
            name = self.form.item(row_idx, 0).text()

            # build entry for exercise
            entry = {"sets": {}}
            updated = False
            for setn, col_idx in enumerate(range(1, 1 + 2 * self.nsets, 2), start=1):
                if (
                    (weight := self.form.item(row_idx, col_idx))
                    and (reps := self.form.item(row_idx, col_idx + 1))
                    and (w := weight.text())
                    and (r := reps.text())
                ):
                    entry["sets"][f"{setn}"] = {"weight": float(w), "reps": int(r)}
                    updated = True

            if updated:
                entry["max_setn"] = int(max(entry["sets"]))
                entry["notes"] = (
                    self.form.item(row_idx, col_idx + 2).text()
                    if self.form.item(row_idx, col_idx + 2)
                    else ""
                )

                # update data
                Parser.add(entry, name, date)

        # print(self.data)
        self.refresh_callback()

        self.accept()

    def _add_row(self):
        # ex_name, ok = QInputDialog.getText(self, "Enter New Exercise", "Name:", QLineEdit.Normal)
        # if ex_name and ok:

        self.form.insertRow(self.nrows - 2)
        self.form.setItem(self.nrows - 2, 0, QTableWidgetItem())
        self.nrows += 1

        self.adjustSize()

    def _add_set_column(self):
        self._set_nsets(self.nsets + 1)

    def _set_nsets(self, nsets):
        if nsets <= 1:
            return

        if nsets > self.nsets:
            for n in range(nsets - self.nsets):
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

            self.ncols += 2 * (nsets - self.nsets)
            self.nsets = nsets

        elif nsets < self.nsets:
            for n in range(self.nsets - nsets):
                self.form.removeColumn(self.ncols - 2 - 2 * n)
                self.form.removeColumn(self.ncols - 3 - 2 * n)

            self.ncols -= 2 * (self.nsets - nsets)
            self.nsets = nsets

        self.adjustSize()


if __name__ == "__main__":
    app = QApplication()
    # entry = ExerciseEntry()
    # entry.add_set_column()
    # entry.show()

    entry = NewEntry([], lambda x: None)
    app.exec()
