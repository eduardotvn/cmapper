from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox

def load_dt_buttons(self, parent):

    self.defaultDataframeLabel = QtWidgets.QLabel(parent)
    self.defaultDataframeLabel.setGeometry(QtCore.QRect(5, 20, 150, 30))
    self.defaultDataframeLabel.setText("Using current dataframe")

    self.dtInfoData = QtWidgets.QTextEdit(parent)
    self.dtInfoData.setGeometry(QtCore.QRect(350, 40, 400, 300))
    
    self.targetColInputLabel = QtWidgets.QLabel(parent)
    self.targetColInputLabel.setGeometry(QtCore.QRect(5, 90, 150, 30))
    self.targetColInputLabel.setText("Target column:")

    self.targetColInputDT =  QtWidgets.QComboBox(parent)
    self.targetColInputDT.setGeometry(QtCore.QRect(160, 90, 150, 30))
    self.targetColInputDT.addItems(self.current_dataframe.columns.tolist())

    self.testSizeInputLabel = QtWidgets.QLabel(parent)
    self.testSizeInputLabel.setGeometry(QtCore.QRect(5, 140, 150, 30))
    self.testSizeInputLabel.setText("Test Size:")

    self.testSizeInputDT =  QtWidgets.QLineEdit(parent)
    self.testSizeInputDT.setGeometry(QtCore.QRect(160, 140, 150, 30))

    self.randomStateInputLabel = QtWidgets.QLabel(parent)
    self.randomStateInputLabel.setGeometry(QtCore.QRect(5, 190, 150, 30))
    self.randomStateInputLabel.setText("Random state:")

    self.randomStateInputDT =  QtWidgets.QLineEdit(parent)
    self.randomStateInputDT.setGeometry(QtCore.QRect(160, 190, 150, 30))

    self.trainDTButton = QtWidgets.QPushButton(parent)
    self.trainDTButton.setGeometry(QtCore.QRect(225, 240, 88, 34))
    self.trainDTButton.setText("Train")

    self.DTDefaultValues = QtWidgets.QLabel(parent)
    self.DTDefaultValues.setGeometry(QtCore.QRect(5, 225, 220, 60))
    self.DTDefaultValues.setText("Use default values:\n(Random State and Test Size)")
    
    self.DTDefaultValuesCB = QtWidgets.QCheckBox(parent)
    self.DTDefaultValuesCB.setGeometry(QtCore.QRect(125, 238, 20, 20))

