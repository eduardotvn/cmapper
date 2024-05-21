from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem

def load_LDA_buttons(self, parent):
    
    self.numComponentsLabel = QtWidgets.QLabel(parent)
    self.numComponentsLabel.setGeometry(QtCore.QRect(5, 30, 150, 30))
    self.numComponentsLabel.setText("Number of components:")

    self.numComponentsInput = QtWidgets.QLineEdit(parent)
    self.numComponentsInput.setGeometry(QtCore.QRect(160, 30, 150, 30))
    
    self.scalerLabel = QtWidgets.QLabel(parent)
    self.scalerLabel.setGeometry(QtCore.QRect(5, 70, 100, 30))
    self.scalerLabel.setText("Scaler:")

    self.scalerOptions = QtWidgets.QComboBox(parent)
    self.scalerOptions.setGeometry(QtCore.QRect(160, 70, 150, 30))
    self.scalerOptions.addItems(["Standard", "MinMax", "MaxAbs"])

    self.generateLDAButton = QtWidgets.QPushButton(parent)
    self.generateLDAButton.setGeometry(QtCore.QRect(222,110, 88,34))
    self.generateLDAButton.setText("Generate")
    self.generateLDAButton.clicked.connect(lambda: generate_LDA_information(self))

    self.kmeansLDAButton = QtWidgets.QPushButton(parent)
    self.kmeansLDAButton.setGeometry(QtCore.QRect(222,150, 88,34))
    self.kmeansLDAButton.setText("K-Means")
    self.kmeansLDAButton.clicked.connect(lambda: run_clusters_dialog(self))

    self.LDAInfoData = QtWidgets.QTableWidget(parent)
    self.LDAInfoData.setGeometry(QtCore.QRect(350, 30, 400, 200))
    self.LDAInfoData.setStyleSheet("border: 1px solid black;")
    if self.processed_dataframe_type == "LDA":
        pass

    self.plotButton = QtWidgets.QPushButton(parent)
    self.plotButton.setGeometry(QtCore.QRect(665, 240, 88, 34))
    self.plotButton.setText("Plot")
    self.plotButton.clicked.connect(lambda: run_plot_widget(self))


def run_plot_widget(self):
    QMessageBox.warning(self.window, "Sorry", "I'm still under development!")
