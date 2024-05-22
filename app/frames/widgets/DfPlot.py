from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np

class PlotWidget(QtWidgets.QDialog):
    def __init__(self, data, labels=None, plot_type='2D', parent=None):
        super().__init__(parent)
        self.setWindowTitle("Plot Dialog")
        self.setGeometry(150, 150, 800, 600)
        
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
        if isinstance(data, pd.DataFrame):
            x = data.iloc[:, 0]
            y = data.iloc[:, 1]
        else:
            x = data[:, 0]
            y = data[:, 1]
        
        if labels is not None:
            scatter = ax.scatter(x, y, c=labels, cmap='viridis')
            legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
            ax.add_artist(legend1)
        else:
            ax.scatter(x, y)
        
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_title('2D Plot')


    def plot_3d(self, data, labels):
        ax = self.figure.add_subplot(111, projection='3d')
        if isinstance(data, pd.DataFrame):
            x = data.iloc[:, 0]
            y = data.iloc[:, 1]
            z = data.iloc[:, 2]
        else:
            x = data[:, 0]
            y = data[:, 1]
            z = data[:, 2]

        if labels is not None:
            scatter = ax.scatter(x, y, z, c=labels, cmap='viridis')
            legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
            ax.add_artist(legend1)
        else:
            ax.scatter(x, y, z)
        
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_zlabel('Component 3')
        ax.set_title('3D Plot')
