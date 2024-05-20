from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ElbowPlotWidget(QWidget):
    def __init__(self, wcss, k_values, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot(wcss, k_values)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, wcss, k_values):
        ax = self.figure.add_subplot(111)
        ax.plot(k_values, wcss, marker='o')
        ax.set_xlabel('Number of clusters')
        ax.set_ylabel('Within-cluster Sum of Squares (WCSS)')
        ax.set_title('Elbow Method for Optimal k')
        self.canvas.draw()
