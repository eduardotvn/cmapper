from PyQt5 import QtCore, QtGui, QtWidgets

def load_plotting_features(self, parent):
    self.running_feature.hide()

    if self.current_dataframe is None:
        self.set_dataframe()

    self.PlottingGB = QtWidgets.QGroupBox(parent)
    self.PlottingGB.setGeometry(QtCore.QRect(210, 30, 811, 521))
    self.PlottingGB.setTitle("")

    self.dataframeOptions = QtWidgets.QComboBox(self.PlottingGB)
    self.dataframeOptions.setGeometry(QtCore.QRect(5, 20, 150, 30))
    self.dataframeOptions.addItems(["Dataframe", "Table"])

    self.running_feature = self.PlottingGB
    self.running_feature.show()

