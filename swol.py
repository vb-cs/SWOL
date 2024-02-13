from PyQt5.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QToolBar,
    QApplication,
    QVBoxLayout,
    QWidget,
    QSplitter,
)

from PyQt5.QtCore import QSize

from PyQt5.QtCore import Qt
from src.dataparser import Parser
from src.actionbar.actionbar import ActionBar

from src.table import Table
from src.visualizer import Visualizer
from src.backend.data import Data

import pandas as pd
import numpy as np


class SWOL(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.table = Table()
        self.visualizer = Visualizer(data)
        action_bar = ActionBar(self, data)

        self.splitter = QSplitter()
        self.splitter.addWidget(self.visualizer)
        self.splitter.addWidget(self.table)
        self.splitter.setOrientation(Qt.Orientation.Vertical)

        self.addToolBar(Qt.BottomToolBarArea, action_bar)
        self.setCentralWidget(self.splitter)
        self.setMinimumSize(QSize(1000, 720))
        self.show()

    def refresh(self):
        self.table.refresh()
        self.visualizer.refresh()

    def closeEvent(self, event):
        # save data
        # Parser.save()

        # close
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])

    Data.load()
    Parser.parse()
    s = SWOL(Parser.data)
    app.exec()
