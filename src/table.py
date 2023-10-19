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
                self.data["exercises"],
                dict().keys(),
            )
        )

        # 1 row for date + weight, rep for every set + 2 space rows between each exercise
        self.setColumnCount(
            1
            + 2 * sum(ex["max_nsets"] for ex in self.data["exercises"])
            + 2 * len(self.data["exercises"])
        )
        self.setRowCount(len(dates) + 2)

        # set headers
        colIndex = 1
        for ex in self.data["exercises"]:
            self.setItem(0, colIndex, QTableWidgetItem(ex["name"]))
            for index in range(0, ex["max_nsets"]):
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

            colIndex += 2 + 2 * ex["max_nsets"]

        # set rows
        for rowIndex, date in enumerate(dates, start=2):
            # add date to row
            self.setItem(rowIndex, 0, QTableWidgetItem(date))

            # add data
            start_index = 1
            for ex in self.data["exercises"]:
                if session_data := ex["data"].get(date):
                    for set_num in range(session_data["nsets"]):
                        if not session_data.get(f"set{set_num+1}"):
                            continue

                        self.setItem(
                            rowIndex,
                            2 * set_num + start_index,
                            QTableWidgetItem(str(session_data[f"set{set_num + 1}"]["weight"])),
                        )
                        self.setItem(
                            rowIndex,
                            2 * set_num + start_index + 1,
                            QTableWidgetItem(str(session_data[f"set{set_num + 1}"]["reps"])),
                        )

                    self.setItem(
                        rowIndex,
                        start_index + 2 * ex["max_nsets"],
                        QTableWidgetItem(session_data["notes"]),
                    )

                start_index += 2 * ex["max_nsets"] + 2


if __name__ == "__main__":
    app = QApplication()
    Parser.parse()
    s = Table(Parser.data)
    app.exec()
