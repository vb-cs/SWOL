import json
import sys
from datetime import date
from functools import reduce

import matplotlib
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QScrollArea
)

from dataparser import Parser

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PySide6.QtWidgets import QApplication, QMainWindow
import matplotlib.dates as mpl_dates


class PlotWidget(QWidget):
    def __init__(self, fig, ax):
        super().__init__()
        self.axes = ax

class CustomWidget(QWidget):
    def __init__(self): 
        super().__init__()


class Visualizer(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        
        self.plot_layout = QGridLayout()
        self.plot_widget = QWidget()
        self.refresh()
        self.plot_widget.setLayout(self.plot_layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.plot_widget)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)


    def refresh(self):
        pass
        """
        graphs = [self._generate_plot(ex) for ex in self.data["exercises"]]
        self.layout

        """

        plots = [self._generate_plot(ex) for ex in self.data["exercises"]]
    
        for i, plot in enumerate(plots):
            self.plot_layout.addWidget(plot)
        

    def _generate_plot(self, ex):
        name = ex["name"]
        max_nsets = ex["max_nsets"]
        data = ex["data"]

        # build lists for each set
        weights = [[] for _ in range(max_nsets)]
        reps = [[] for _ in range(max_nsets)]
        dates = [[] for _ in range(max_nsets)]

        # extract data for this exercise
        for d, log in data.items():
            for set_idx in range(log["nsets"]):
                weights[set_idx].append(log[f"set{set_idx + 1}"]["weight"])
                reps[set_idx].append(log[f"set{set_idx + 1}"]["reps"])
                dates[set_idx].append(date.fromisoformat(d))

        # plot
        plt.figure()
        plt.plot(dates[0], weights[0])
        print(dates[0], weights[0])
        plt.title(name)
        plt.ylabel("Weight")
        date_fmt = mpl_dates.DateFormatter("%b. %d %Y")
        fig, ax = plt.gcf(), plt.gca()

        fig.autofmt_xdate()
        ax.xaxis.set_major_formatter(date_fmt)

        if len(dates[0]) <= 1: 
            ax.set_xticks(dates[0])
        if len(dates[0]) > 1 and len(dates[0]) < 6:
            ax.xaxis.set_major_locator(mpl_dates.DayLocator(interval=1))
        plt.tight_layout()

        # return fig, axes
        return FigureCanvasQTAgg(fig)


if __name__ == "__main__":
    data = {
        "exercises": [
            {
                "name": "OHP",
                "max_nsets": 2,
                "data": {
                    "2023-10-13": {
                        "nsets": 2,
                        "set1": {"weight": 40, "reps": 10},
                        "set2": {"weight": 40, "reps": 10},
                        "notes": "",
                    }
                },
            },
            {
                "name": "Preacher Curls",
                "max_nsets": 1,
                "data": {
                    "2023-10-11": {
                        "nsets": 1,
                        "set1": {"weight": 25, "reps": 7},
                        "notes": "Left hand",
                    },
                    "2023-10-13": {
                        "nsets": 1,
                        "set1": {"weight": 25, "reps": 7},
                        "notes": "Left hand",
                    },
                },
            },
        ]
    }
    app = QApplication()

    v = Visualizer(data)
    v.show()
    app.exec()