import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets

class DataFramePiePlotWidget(QtWidgets.QWidget):
    def __init__(self, dataframe=None, column=None, parent=None):
        super(DataFramePiePlotWidget, self).__init__(parent)
        self.dataframe = dataframe
        self.column = column
        self.figure = None
        self.canvas = None
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.plot()

    def plot(self):
        if self.figure:
            plt.close(self.figure)
        
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        
        if self.dataframe is not None and self.column is not None:
            self.figure = plt.figure()
            self.canvas = FigureCanvas(self.figure)
            self.layout.addWidget(self.canvas)
            ax = self.figure.add_subplot(111)
            pie_data = self.dataframe[self.column].value_counts()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            self.canvas.draw()

def show_pie_options(self):
    self.pieGB = QtWidgets.QGroupBox(self.PlottingGB)
    self.pieGB.setGeometry(5, 170, 250, 300)
    self.pieGB.setStyleSheet("QGroupBox { border: 0; }")

    self.columnLabel = QtWidgets.QLabel(self.pieGB)
    self.columnLabel.setGeometry(QtCore.QRect(0, 0, 150, 30))
    self.columnLabel.setText("Select column to plot")

    self.columnComboBox = QtWidgets.QComboBox(self.pieGB)
    self.columnComboBox.addItems(self.current_dataframe.columns.tolist())
    self.columnComboBox.setGeometry(QtCore.QRect(0, 30, 150, 30))
    self.columnComboBox.currentIndexChanged.connect(lambda: show_pie_plot(self))

    if self.running_plot_feature != self.pieGB:
        if self.running_plot_feature is not None:
            self.running_plot_feature.hide()
        self.running_plot_feature = self.pieGB
        self.pieGB.show()

def show_pie_plot(self):
    selected_column = self.columnComboBox.currentText()
    
    if selected_column:
        if hasattr(self, 'plot_widget') and self.plot_widget is not None:
            self.plot_widget.close()
            
        self.plot_widget = DataFramePiePlotWidget(
            dataframe=self.current_dataframe,
            column=selected_column,
            parent=self.PlottingGB
        )
        self.plot_widget.setGeometry(self.PlottingVisualizationGB.geometry())
        self.plot_widget.show()
