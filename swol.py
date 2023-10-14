from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QToolBar,
    QApplication,
    QVBoxLayout,
)

from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtCore import Qt
from dataparser import Parser
from actionbar import ActionBar

from table import Table


class SWOL(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.table = Table(data)
        action_bar = ActionBar(self, data)

        self.addToolBar(Qt.BottomToolBarArea, action_bar)
        self.setCentralWidget(self.table)

        self.show()

    def closeEvent(self, event):
        # save data
        #Parser.save()

        # close
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication()
    Parser.parse()
    s = SWOL(Parser.data)
    app.exec()
