import sys

import pandas as pd
import numpy as np 
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QLabel, QWidget, QVBoxLayout


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col][0]

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()

        exercises = ["OHP", "Squat", "Deadlift"]
        sets = [
            [ex for ex, n_sets in zip(exercises, (2, 3, 1)) for _ in range(2 * n_sets + 1)],
            [
                "Set 1 Weight",
                "Set 1 Reps",
                "Set 2 Weight",
                "Set 2 Reps",
                "Notes",
                "Set 1 Weight",
                "Set 1 Reps",
                "Set 2 Weight",
                "Set 2 Reps",
                "Set 3 Weight",
                "Set 3 Reps",
                "Notes",
                "Set 1 Weight",
                "Set 1 Reps",
                "Notes",
            ],
        ]

        dates = ["2023-1-1", "2023-1-2", "2023-1-3"]

        columns = pd.MultiIndex.from_arrays(sets)

        df = pd.DataFrame(np.random.randn(3, 15), index=dates, columns=columns)
        print(df)

        self.model = PandasModel(df)
        self.table.setModel(self.model)

        self.title = QLabel("OHP")
        self.printbutton = QPushButton("Print")
        self.printbutton.clicked.connect(lambda _: print(df))

        self.mainwidget = QWidget()
        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(self.title)
        self.mainlayout.addWidget(self.table)
        self.mainlayout.addWidget(self.printbutton)

        self.mainwidget.setLayout(self.mainlayout)

        self.setCentralWidget(self.mainwidget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
