from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from utils.applyLDA import apply_lda

def load_LDA_buttons(self, parent):
    
    self.numComponentsLabel = QtWidgets.QLabel(parent)
    self.numComponentsLabel.setGeometry(QtCore.QRect(5, 30, 150, 30))
    self.numComponentsLabel.setText("Number of components:")

    self.numComponentsInput = QtWidgets.QLineEdit(parent)
    self.numComponentsInput.setGeometry(QtCore.QRect(160, 30, 150, 30))
    
    self.scalerLabel = QtWidgets.QLabel(parent)
    self.scalerLabel.setGeometry(QtCore.QRect(5, 65, 100, 30))
    self.scalerLabel.setText("Scaler:")

    self.scalerOptions = QtWidgets.QComboBox(parent)
    self.scalerOptions.setGeometry(QtCore.QRect(160, 65, 150, 30))
    self.scalerOptions.addItems(["Standard", "MinMax", "MaxAbs"])

    self.targetLabel = QtWidgets.QLabel(parent)
    self.targetLabel.setGeometry(QtCore.QRect(5, 100, 100, 30))
    self.targetLabel.setText("Target Col:") 

    self.targetColCB = QtWidgets.QComboBox(parent)
    self.targetColCB.setGeometry(QtCore.QRect(160, 100, 150, 30))
    self.targetColCB.addItems(self.current_dataframe.columns.tolist())

    self.generateLDAButton = QtWidgets.QPushButton(parent)
    self.generateLDAButton.setGeometry(QtCore.QRect(222,140, 88,34))
    self.generateLDAButton.setText("Generate")
    self.generateLDAButton.clicked.connect(lambda: generate_LDA_information(self))

    self.LDAInfoData = QtWidgets.QTableWidget(parent)
    self.LDAInfoData.setGeometry(QtCore.QRect(350, 30, 400, 200))
    self.LDAInfoData.setStyleSheet("border: 1px solid black;")
    if self.processed_dataframe_type == "LDA":
        pass

    self.plotButton = QtWidgets.QPushButton(parent)
    self.plotButton.setGeometry(QtCore.QRect(665, 240, 88, 34))
    self.plotButton.setText("Plot")
    self.plotButton.clicked.connect(lambda: run_plot_widget(self))

    self.accLabel = QtWidgets.QLabel(parent)
    self.accLabel.setGeometry(QtCore.QRect(350, 230, 250, 30))


def run_plot_widget(self):
    QMessageBox.warning(self.window, "Sorry", "I'm still under development!")

def generate_LDA_information(self):
    target = self.targetColCB.currentText()
    dataframe = self.current_dataframe.copy()
    num_components = self.numComponentsInput.text()
    scaler = self.scalerOptions.currentText()

    if num_components == '':
        QMessageBox.warning(self.window, "Invalid value", "Insert a valid number of components")
        return
    elif int(num_components) > len(self.current_dataframe.columns.tolist()) or int(num_components) <= 0:
        QMessageBox.warning(self.window, "Invalid value", "Insert a valid number of components")
        return 
    num_components = int(num_components)

    results, acc, err = apply_lda(dataframe, num_components, scaler, target)

    if err is not None:
        QMessageBox.critical(self.window, "Error", f"{str(err)}")
    else: 
        dataframe['Predictions'] = results
        self.processed_dataframe = dataframe
        self.processed_dataframe_type = "LDA"
        self.accLabel.setText(f"Accuracy: {acc:.4f}")
        self.populate_pca_table()
