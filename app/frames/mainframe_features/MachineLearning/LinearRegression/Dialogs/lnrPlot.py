import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout


class LinearRegressionDialog(QDialog):
    def __init__(self, X_test, y_test, y_pred):
        super().__init__()

        self.setWindowTitle("Linear Regression Model")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.canvas = PlotCanvas(self, width=6, height=4)
        layout.addWidget(self.canvas)

        self.plot_linear_regression(X_test, y_test, y_pred)

    def plot_linear_regression(self, X_test, y_test, y_pred):
        if isinstance(y_test, (pd.DataFrame, pd.Series)):
            y_test = y_test.values

        plt.figure()
        plt.scatter(X_test, y_test, color='blue', label='Test Data')
        plt.plot(X_test, y_pred, color='red', linewidth=2, label='Linear Regression Model')
        plt.xlabel('X_test')
        plt.ylabel('y_test / Predictions')
        plt.title('Linear Regression Model')
        plt.legend()
        self.canvas.draw()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
