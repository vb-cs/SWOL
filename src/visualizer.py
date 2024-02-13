from datetime import date

from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QScrollArea, 
    QSizePolicy
)
from PyQt5.QtWidgets import QApplication, QMainWindow
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.dates as mpl_dates
import pandas as pd

from .dataparser import Parser
from .backend.data import Data

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
        for exercise in Data.exercises():
            self.plots[exercise] = self._load_plot(exercise, self.plots.get(exercise))
        
        for plot in self.plots.values(): 
            self.plot_layout.addWidget(plot)
        

    def _load_plot(self, exercise, plot=None):
        if not plot:
            fig = plt.figure(figsize=(5,3.5))
            ax = fig.add_subplot()
            plot = PlotWidget(fig, ax)

        plot.clear()

        plot.axes.plot([date.fromisoformat(d) for d in Data.df.loc[:, (exercise, "Set 1 Weight")].index], Data.df.loc[:, (exercise, "Set 1 Weight")])
        plot.axes.set_title(exercise)
        plot.axes.set_ylabel("Weight")

        date_fmt = mpl_dates.DateFormatter("%b. %d %Y")
        plot.fig.autofmt_xdate()
        plot.axes.xaxis.set_major_formatter(date_fmt)        
        plot.fig.tight_layout()

        plot.draw()

        return plot


if __name__ == "__main__":
    data = pd.DataFrame()
    app = QApplication()

    v = Visualizer(data)
    v.show()
    app.exec()
