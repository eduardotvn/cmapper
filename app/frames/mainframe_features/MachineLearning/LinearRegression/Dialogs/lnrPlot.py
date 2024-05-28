import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout

class LinearRegressionDialog(QDialog):
    def __init__(self, X_test, y_test, y_pred):
        super().__init__()

        self.setWindowTitle("Linear Regression Model")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.canvas = PlotCanvas(self, X_test, y_test, y_pred, width=6, height=4)
        layout.addWidget(self.canvas)

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, X_test=None, y_test=None, y_pred=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

        self.plot_linear_regression(X_test, y_test, y_pred)

    def plot_linear_regression(self, X_test, y_test, y_pred):
        if isinstance(y_test, (pd.DataFrame, pd.Series)):
            y_test = y_test.values
        if isinstance(X_test, (pd.DataFrame, pd.Series)):
            X_test = [value[0] for value in X_test.values]

        print(f"X_test: {X_test}\ny_test: {y_test}\ny_pred: {y_pred}")
        print(f"X_test len: {len(X_test)}\ny_test len:{len(y_test)}\ny_pred len: {len(y_pred)}")

        self.ax.clear()  
        self.ax.scatter(X_test, y_test, color='blue', label='Test Data')
        self.ax.plot(X_test, y_pred, color='red', linewidth=2, label='Linear Regression Model')
        self.ax.set_xlabel('X_test')
        self.ax.set_ylabel('y_test / Predictions')
        self.ax.set_title('Linear Regression Model')
        self.ax.legend()
        self.draw()