import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from utils.applyPCA import apply_pca, elbow_method
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from .Dialogs.NumClustersDialog import Ui_ClustersDialog

def load_pca_buttons(self, parent):
    
    self.numComponentsLabel = QtWidgets.QLabel(parent)
    self.numComponentsLabel.setGeometry(QtCore.QRect(5, 50, 150, 30))
    self.numComponentsLabel.setText("Number of components:")

    self.numComponentsInput = QtWidgets.QLineEdit(parent)
    self.numComponentsInput.setGeometry(QtCore.QRect(160, 50, 150, 30))
    
    self.scalerLabel = QtWidgets.QLabel(parent)
    self.scalerLabel.setGeometry(QtCore.QRect(5, 90, 100, 30))
    self.scalerLabel.setText("Scaler:")

    self.scalerOptions = QtWidgets.QComboBox(parent)
    self.scalerOptions.setGeometry(QtCore.QRect(160, 90, 150, 30))
    self.scalerOptions.addItems(["Standard", "MinMax", "MaxAbs"])

    self.generatePCAButton = QtWidgets.QPushButton(parent)
    self.generatePCAButton.setGeometry(QtCore.QRect(222,130, 88,34))
    self.generatePCAButton.setText("Generate")
    self.generatePCAButton.clicked.connect(lambda: generate_pca_information(self))

    self.kmeansPCAButton = QtWidgets.QPushButton(parent)
    self.kmeansPCAButton.setGeometry(QtCore.QRect(222,170, 88,34))
    self.kmeansPCAButton.setText("K-Means")
    self.kmeansPCAButton.clicked.connect(lambda: run_clusters_dialog(self))

    self.PCAInfoData = QtWidgets.QTableWidget(parent)
    self.PCAInfoData.setGeometry(QtCore.QRect(350, 50, 400, 200))
    self.PCAInfoData.setStyleSheet("border: 1px solid black;")
    if self.processed_dataframe_type == "pca":
        self.populate_pca_table()

    self.evrLabel = QtWidgets.QLabel(parent)
    self.evrLabel.setGeometry(QtCore.QRect(350, 250, 250, 30))

def generate_pca_information(self):
    scaler = self.scalerOptions.currentText()
    if self.numComponentsInput.text() == '':
        n_comps = 0
    else:
        n_comps = int(self.numComponentsInput.text())

    if n_comps > len(self.current_dataframe.columns.tolist()) or n_comps <= 0:        
            QMessageBox.warning(self.window, "Warning", f"Choose a value between 1 and {len(self.current_dataframe.columns.tolist())}")
            return
    if scaler is None: 
            QMessageBox.warning(self.window, "Warning", "Choose a scaler")
            return 

    df, evr, error = apply_pca(self.current_dataframe, scaler, n_comps)

    if df is not None: 
        self.processed_dataframe = df 
        self.processed_dataframe_type = "pca"
        self.evrLabel.setText(f"Explained Variance Ratio: {evr[0]:.4f}")
        self.populate_pca_table()
    elif error: 
        QMessageBox.critical(self.window, "Error", f"{str(e)}")


def run_clusters_dialog(self):
    if self.processed_dataframe is not None and self.processed_dataframe_type == "pca":
        self.Clusters_Dialog = QtWidgets.QDialog()
        self.CluDialog = Ui_ClustersDialog()
        self.CluDialog.setupUi(self.Clusters_Dialog)
        self.CluDialog.parent = self
        self.Clusters_Dialog.show()
    else:
        QMessageBox.warning(self.window, "Error", "Generate a PCA dataframe before proceeding.")