from PyQt5 import QtCore, QtGui, QtWidgets
from frames.mainframe_features.DataframeEdit.Dialogs.DataFrameHead import DataFrameDialog
from .plotFuncs.linePlot import show_line_options
from .plotFuncs.barPlot import show_bar_options
from .plotFuncs.piePlot import show_pie_options

def load_plotting_features(self, parent):
    self.running_feature.hide()

    self.running_plot_feature = None

    if self.current_dataframe is None:
        self.set_dataframe()

    self.PlottingGB = QtWidgets.QGroupBox(parent)
    self.PlottingGB.setGeometry(QtCore.QRect(210, 30, 811, 521))
    self.PlottingGB.setTitle("")

    self.dataframeOptions = QtWidgets.QComboBox(self.PlottingGB)
    self.dataframeOptions.setGeometry(QtCore.QRect(5, 20, 150, 30))
    self.dataframeOptions.addItems(["Dataframe", "Table"])

    self.PlottingVisualizationGB = QtWidgets.QGroupBox(self.PlottingGB)
    self.PlottingVisualizationGB.setGeometry(QtCore.QRect(200, 10, 600, 500))
    self.PlottingVisualizationGB.setStyleSheet("border: 1px solid black;")

    self.previewButtonPLT = QtWidgets.QPushButton(self.PlottingGB)
    self.previewButtonPLT.setGeometry(QtCore.QRect(5, 70, 88, 34))
    self.previewButtonPLT.setText("Preview")
    self.previewButtonPLT.clicked.connect(lambda: show_dataframe_sample(self))

    self.plottingOptions = QtWidgets.QComboBox(self.PlottingGB)
    self.plottingOptions.setGeometry(QtCore.QRect(5, 120, 150, 30))
    self.plottingOptions.addItems(plot_options)
    self.plottingOptions.currentIndexChanged.connect(lambda: show_plot_options(self))



    self.running_feature = self.PlottingGB
    self.running_feature.show()

def show_dataframe_sample(self):
    df_sample = self.current_dataframe.head()
    self.dialog = DataFrameDialog(df_sample)
    self.dialog.exec_()

def show_plot_options(self):
    if self.plottingOptions.currentText() == "Line":
        show_line_options(self)
    elif self.plottingOptions.currentText() == "Bar":
        show_bar_options(self)
    elif self.plottingOptions.currentText() == "Pie":
        show_pie_options(self)
    elif self.plottingOptions.currentText() == "":
        self.running_plot_feature.hide()

plot_options = ["", "Line", "Bar", "Pie"]