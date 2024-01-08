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

from .dataparser import Parser
from functools import reduce


# class Table(QTableWidget):
#    def sizeHint(self):
#            horizontal = self.horizontalHeader()
#            vertical = self.verticalHeader()
#            frame = self.frameWidth() * 2
#            return QSize(horizontal.length() + vertical.width() + frame,
#                        vertical.length() + horizontal.height() + frame)
#
#    pass


class Table(QTableWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.refresh()
        self.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)

    def refresh(self):
        # Combine data keys
        self.clear()
        dates = sorted(
            reduce(
                lambda curr_keys, ex_dict: curr_keys | ex_dict["data"].keys(),
                self.data["exercises"].values(),
                dict().keys(),
            )
        )

        # 1 row for date + weight, rep for every set + 2 space rows between each exercise
        self.setColumnCount(
            1
            + 2 * sum(ex["max_setn"] for ex in self.data["exercises"].values())
            + 2 * len(self.data["exercises"])
        )
        self.setRowCount(len(dates) + 2)

        # set headers
        colIndex = 1
        for name, ex in self.data["exercises"].items():
            self.setItem(0, colIndex, QTableWidgetItem(name))
            for index in range(0, ex["max_setn"]):
                self.setItem(
                    1,
                    colIndex + 2 * index,
                    QTableWidgetItem(f"Set {index + 1} Weight"),
                )
                self.setItem(
                    1,
                    colIndex + 2 * index + 1,
                    QTableWidgetItem(f"Set {index + 1} Reps"),
                )
                self.setItem(1, colIndex + 2 * index + 2, QTableWidgetItem("Notes"))

            colIndex += 2 + 2 * ex["max_setn"]

        # set rows
        for rowIndex, date in enumerate(dates, start=2):
            # add date to row
            self.setItem(rowIndex, 0, QTableWidgetItem(date))

            # add data
            start_index = 1
            for ex in self.data["exercises"].values():
                if session_data := ex["data"].get(date):
                    for set_num, st in session_data["sets"].items():

                        self.setItem(
                            rowIndex,
                            2 * (int(set_num)- 1) + start_index,
                            QTableWidgetItem(str(st["weight"])),
                        )
                        self.setItem(
                            rowIndex,
                            2 * (int(set_num) - 1) + start_index + 1,
                            QTableWidgetItem(str(st["reps"])),
                        )

                    self.setItem(
                        rowIndex,
                        start_index + 2 * ex["max_setn"],
                        QTableWidgetItem(session_data["notes"]),
                    )

                start_index += 2 * ex["max_setn"] + 2


if __name__ == "__main__":
    app = QApplication()
    Parser.parse()
    s = Table(Parser.data)
    app.exec()
