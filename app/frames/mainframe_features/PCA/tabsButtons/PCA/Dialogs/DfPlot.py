from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D 

class PlotWidget(QWidget):
    def __init__(self, data, labels=None, plot_type='2D', parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot(data, labels, plot_type)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, data, labels, plot_type):
        self.figure.clear()  

        if plot_type == '2D':
            self.plot_2d(data, labels)
        elif plot_type == '3D':
            self.plot_3d(data, labels)
        else:
            raise ValueError("plot_type must be '2D' or '3D'")

        self.canvas.draw()

    def plot_2d(self, data, labels):
        ax = self.figure.add_subplot(111)
        if labels is not None:
            scatter = ax.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis')
            legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
            ax.add_artist(legend1)
        else:
            ax.scatter(data[:, 0], data[:, 1])
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_title('2D Plot')

    def plot_3d(self, data, labels):
        ax = self.figure.add_subplot(111, projection='3d')
        if labels is not None:
            scatter = ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=labels, cmap='viridis')
            legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
            ax.add_artist(legend1)
        else:
            ax.scatter(data[:, 0], data[:, 1], data[:, 2])
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_zlabel('Component 3')
        ax.set_title('3D Plot')
