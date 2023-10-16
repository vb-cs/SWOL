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
)

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QSize
import json
from datetime import date

from dataparser import Parser
from functools import reduce