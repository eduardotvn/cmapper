import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets

class DataFrameBarPlotWidget(QtWidgets.QWidget):
    def __init__(self, dataframe=None, columns=None, target_column=None, parent=None):
        super(DataFrameBarPlotWidget, self).__init__(parent)
        self.dataframe = dataframe
        self.columns = columns
        self.target_column = target_column
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
        
        if self.dataframe is not None and self.columns is not None and self.target_column is not None:
            self.figure = plt.figure()
            self.canvas = FigureCanvas(self.figure)
            self.layout.addWidget(self.canvas)
            ax = self.figure.add_subplot(111)
            sorted_df = self.dataframe.sort_values(by=[self.target_column])
            for column in self.columns:
                if column != self.target_column:
                    ax.bar(sorted_df[self.target_column], sorted_df[column], label=column)
            ax.set_xlabel(self.target_column)
            ax.set_ylabel('Values')
            ax.legend()
            self.canvas.draw()

def show_bar_options(self):
    self.barGB = QtWidgets.QGroupBox(self.PlottingGB)
    self.barGB.setGeometry(5, 140, 250, 300)
    self.barGB.setStyleSheet("QGroupBox { border: 0; }")

    self.targetColLabel = QtWidgets.QLabel(self.barGB)
    self.targetColLabel.setGeometry(QtCore.QRect(0, 0, 150, 30))
    self.targetColLabel.setText("Set a column as X axis")

    self.targetColPlot = QtWidgets.QComboBox(self.barGB)
    self.targetColPlot.addItems(self.current_dataframe.columns.tolist())
    self.targetColPlot.setGeometry(QtCore.QRect(0, 30, 150, 30))
    self.targetColPlot.currentIndexChanged.connect(lambda: show_bar_plot(self))

    self.columnsLabel = QtWidgets.QLabel(self.barGB)
    self.columnsLabel.setGeometry(QtCore.QRect(0, 60, 150, 30))
    self.columnsLabel.setText("Select columns to plot")

    self.columnsList = QtWidgets.QListWidget(self.barGB)
    self.columnsList.addItems(self.current_dataframe.columns.tolist())
    self.columnsList.setGeometry(QtCore.QRect(0, 90, 150, 150))
    self.columnsList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    self.columnsList.itemSelectionChanged.connect(lambda: show_bar_plot(self))

    if self.running_plot_feature != self.barGB:
        if self.running_plot_feature is not None:
            self.running_plot_feature.hide()
        self.running_plot_feature = self.barGB
        self.barGB.show()

def show_bar_plot(self):
    selected_target_column = self.targetColPlot.currentText()
    selected_columns = [item.text() for item in self.columnsList.selectedItems()]
    
    if selected_target_column and selected_columns:
        if hasattr(self, 'plot_widget') and self.plot_widget is not None:
            self.plot_widget.close()
            
        self.plot_widget = DataFrameBarPlotWidget(
            dataframe=self.current_dataframe,
            columns=selected_columns,
            target_column=selected_target_column,
            parent=self.PlottingGB
        )
        self.plot_widget.setGeometry(self.PlottingVisualizationGB.geometry())
        self.plot_widget.show()
