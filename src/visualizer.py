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
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QScrollArea, 
    QLayout,
    QSizePolicy
)


from .dataparser import Parser

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PySide6.QtWidgets import QApplication, QMainWindow
import matplotlib.dates as mpl_dates


class PlotWidget(FigureCanvasQTAgg):
    def __init__(self, fig, ax):
        super().__init__(fig)
        self.fig = fig
        self.axes = ax
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.updateGeometry()
        

    def clear(self):
        self.axes.cla()


class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()


class Visualizer(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data

        #self.plot_layout = QGridLayout()
        
        #self.plot_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.plot_layout = QHBoxLayout()
        self.container = QWidget()
        self.plots = {}

        self.plot_layout.addStretch()
        self.refresh()
        self.plot_layout.addStretch()
        self.container.setLayout(self.plot_layout)
        #self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.container)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)

    def refresh(self):
        for name, ex in self.data["exercises"].items():
            self.plots[name] = self._load_plot(name, ex, self.plots.get(name))
        
        for plot in self.plots.values(): 
            self.plot_layout.addWidget(plot)
        

    def _load_plot(self, title, ex, plot=None):
        max_setn = ex["max_setn"]
        data = ex["data"]

        # build lists for each set
        weights = [[] for _ in range(max_setn)]
        reps = [[] for _ in range(max_setn)]
        dates = [[] for _ in range(max_setn)]

        # extract data for this exercise
        for d, log in data.items():
            for setn, s in log["sets"].items():
                set_idx = int(setn) - 1
                weights[set_idx].append(s["weight"])
                reps[set_idx].append(s["reps"])
                dates[set_idx].append(date.fromisoformat(d))

        # plot
        if not plot:
            fig = plt.figure(figsize=(5,3.5))
            ax = fig.add_subplot()
            plot = PlotWidget(fig, ax)

        plot.clear()

        plot.axes.plot(dates[0], weights[0])
        # print(dates[0], weights[0])
        plot.axes.set_title(title)
        plot.axes.set_ylabel("Weight")

        date_fmt = mpl_dates.DateFormatter("%b. %d %Y")
        plot.fig.autofmt_xdate()

        plot.axes.xaxis.set_major_formatter(date_fmt)

        
        plot.fig.tight_layout()
        plot.draw()



        return plot


if __name__ == "__main__":
    #if len(dates[0]) <= 1:
    #    plot.axes.set_xticks(dates[0])
    #elif len(dates[0]) > 1 and len(dates[0]) < 6:
    #    plot.axes.xaxis.set_major_locator(mpl_dates.DayLocator(interval=1))
    #else:
    #    plot.axes.xaxis.set_major_locator(mpl_dates.AutoDateLocator())
    data = {
        "exercises": [
            {
                "name": "OHP",
                "max_setn": 2,
                "data": {
                    "2023-10-13": {
                        "max_setn": 2,
                        "set1": {"weight": 40, "reps": 10},
                        "set2": {"weight": 40, "reps": 10},
                        "notes": "",
                    }
                },
            },
            {
                "name": "Preacher Curls",
                "max_setn": 1,
                "data": {
                    "2023-10-11": {
                        "max_setn": 1,
                        "set1": {"weight": 25, "reps": 7},
                        "notes": "Left hand",
                    },
                    "2023-10-13": {
                        "max_setn": 1,
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
