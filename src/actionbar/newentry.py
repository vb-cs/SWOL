from PyQt5.QtWidgets import (
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
    QListWidget,
    QAction,
)

from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np

from datetime import date
from pathlib import Path
from functools import reduce

from ..backend.data import Data


class ExerciseEntry(QWidget):
    def __init__(self, exercise="", nsets=1):
        super().__init__()

        self.mainLayout = QHBoxLayout()
        self.exerciseEdit = QLineEdit(exercise)
        self.weightEdits = []
        self.repsEdits = []
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
        for _ in range(nsets):
            self.add_set_column()
        self.mainLayout.addWidget(self.notes)
        self.mainLayout.addWidget(self.system)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setLayout(self.mainLayout)

    def add_set_column(self):
        weightEdit = QLineEdit()
        repsEdit = QLineEdit()

        self.mainLayout.insertWidget(1 + 2 * len(self.weightEdits), weightEdit)
        self.mainLayout.insertWidget(2 + 2 * len(self.weightEdits), repsEdit)

        self.weightEdits.append(weightEdit)
        self.repsEdits.append(repsEdit)

    def exercise(self):
        return self.exerciseEdit.text()

    def values(self):
        return (
            *(
                val
                for weightEdit, repEdit in zip(self.weightEdits, self.repsEdits)
                for val in (weightEdit.text(), repEdit.text())
            ),
            self.notes.text(),
        )


class NewEntry(QDialog):
    def __init__(self, data, table):
        super().__init__()
        self.table = table
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
        self.header.addWidget(QWidget())
        self.header.addWidget(QWidget())

        self.exercise_entries = []
        self.form = QVBoxLayout()
        self._init_form()

        self.dateEdit = QLineEdit()
        self.footer = QHBoxLayout()
        self.footer.addWidget(QLabel("Date"))
        self.footer.addWidget(self.dateEdit)
        self.footer.addStretch()

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
        self.mainLayout.addLayout(self.header)
        self.mainLayout.addLayout(self.form)
        self.mainLayout.addLayout(self.footer)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

    def _init_form(self):
        if len(self.exercise_entries) == 0:
            entry = ExerciseEntry()
            self.form.addWidget(entry)
            self.exercise_entries.append(entry)
        else:
            self.exercise_entries = [ExerciseEntry(ex) for ex in Data.exercises()]
            for entry in self.exercise_entries:
                self.form.addWidget(entry)

    def _save(self):
        exercise_names = [name for entry in self.exercise_entries if (name := entry.exercise())]
        exercise_headers = [
            ex_name for ex_name in exercise_names for _ in range(2 * self.nsets + 1)
        ]
        weight_reps_notes = []
        for _ in exercise_names:
            for i in range(1, self.nsets + 1):
                weight_reps_notes.extend((f"Set {i} Weight", f"Set {i} Reps"))
            weight_reps_notes.append("Notes")

        sets = [exercise_headers, weight_reps_notes]
        dates = [self.dateEdit.text()]
        columns = pd.MultiIndex.from_arrays(sets)
        values = np.array(
            [val for entry in self.exercise_entries for val in entry.values()]
        ).reshape((1, 1 + self.nsets * 2))

        new_df = pd.DataFrame(values, index=dates, columns=columns)
        print(new_df)
        self.table.mdl.beginResetModel()
        Data.merge(new_df)
        print(self.table.mdl._data)
        print(self.table.data)
        self.accept()

    def _add_row(self):
        entry = ExerciseEntry(nsets=self.nsets)
        self.exercise_entries.append(entry)
        self.form.addWidget(entry)

        self.adjustSize()

    def _add_set_column(self):
        self.nsets += 1
        for entry in self.exercise_entries:
            entry.add_set_column()

        self.header.insertWidget(-1 + 2 * self.nsets, QLabel(f"Set {self.nsets} Weight"))
        self.header.insertWidget(2 * self.nsets, QLabel(f"Set {self.nsets} Reps"))


if __name__ == "__main__":
    app = QApplication()
    # entry = ExerciseEntry()
    # entry.add_set_column()
    # entry.show()

    entry = NewEntry([], lambda x: None)
    app.exec()
