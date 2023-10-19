from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QToolBar,
    QApplication,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import QSize

from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtCore import Qt
from dataparser import Parser
from actionbar import ActionBar

from table import Table
from visualizer import Visualizer


class SWOL(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.table = Table(data)
        self.visualizer = Visualizer(data)
        action_bar = ActionBar(self, data)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.visualizer)
        self.layout.addWidget(self.table)

        self.main_window = QWidget()
        self.main_window.setLayout(self.layout)

        self.addToolBar(Qt.BottomToolBarArea, action_bar)
        self.setCentralWidget(self.main_window)
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
    app = QApplication()
    Parser.parse()
    s = SWOL(Parser.data)
    app.exec()
