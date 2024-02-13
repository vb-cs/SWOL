import sys
import json
from datetime import date
from functools import reduce

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QToolBar,
    QApplication,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QTableView,
    QAction,
)
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from pandasgui.widgets import dataframe_viewer
import pandas as pd

from .backend.data import Data
from .dataparser import Parser


class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.viewer = dataframe_viewer.DataFrameViewer(Data.df)
        # self.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.viewer)
        self.setLayout(self.mainLayout)

    def refresh(self):
        self.update()


if __name__ == "__main__":
    app = QApplication()

    s = Table()
    app.exec()
