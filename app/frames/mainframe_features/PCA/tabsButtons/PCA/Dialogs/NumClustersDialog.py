from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from utils.applyPCA import elbow_method, apply_kmeans
from .ElbowPlot import ElbowPlotWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Ui_ClustersDialog(object):
    def __init__(self):
        self.parent = None

    def setupUi(self, ClustersDialog):
        ClustersDialog.setObjectName("ClustersDialog")
        ClustersDialog.resize(402, 117)

        self.NumClustersLabel = QtWidgets.QLabel(ClustersDialog)
        self.NumClustersLabel.setGeometry(QtCore.QRect(10, 20, 131, 31))
        self.NumClustersLabel.setObjectName("NumClustersLabel")

        self.NumClustersInput = QtWidgets.QLineEdit(ClustersDialog)
        self.NumClustersInput.setGeometry(QtCore.QRect(160, 20, 113, 32))
        self.NumClustersInput.setObjectName("NumClustersInput")

        self.ElbowMethodButton = QtWidgets.QPushButton(ClustersDialog)
        self.ElbowMethodButton.setGeometry(QtCore.QRect(290, 20, 101, 34))
        self.ElbowMethodButton.setObjectName("ElbowMethodButton")
        self.ElbowMethodButton.clicked.connect(self.display_elbow_method)

        self.GenerateButton = QtWidgets.QPushButton(ClustersDialog)
        self.GenerateButton.setGeometry(QtCore.QRect(0, 80, 88, 34))
        self.GenerateButton.setObjectName("GenerateButton")
        self.GenerateButton.clicked.connect(lambda: self.generate_button(ClustersDialog))

        self.CancelButton = QtWidgets.QPushButton(ClustersDialog)
        self.CancelButton.setGeometry(QtCore.QRect(310, 80, 88, 34))
        self.CancelButton.setObjectName("CancelButton")
        self.CancelButton.clicked.connect(ClustersDialog.close)

        self.retranslateUi(ClustersDialog)
        QtCore.QMetaObject.connectSlotsByName(ClustersDialog)


    def display_elbow_method(self):
        if self.parent.processed_dataframe is not None and self.parent.processed_dataframe_type == "pca":
            df = self.parent.processed_dataframe.copy()
            wcss, k = elbow_method(df)
            
            print(wcss, k)
            self.elbow_plot_widget = ElbowPlotWidget(wcss, k)
            self.elbow_plot_widget.setWindowTitle("Elbow Method Plot")
            self.elbow_plot_widget.resize(800, 600)
            self.elbow_plot_widget.show()
            
    def generate_button(self, window):
        if self.parent.processed_dataframe is not None and self.parent.processed_dataframe_type == "pca":
            num_clusters = self.NumClustersInput.text()
            if num_clusters == '':
                QMessageBox.warning(self.parent.window, "Invalid number", "Input a valid number of clusters")
                return 
            else:
                num_clusters = int(self.NumClustersInput.text())
            if num_clusters <= 0:
                QMessageBox.warning(self.parent.window, "Invalid number", "Choose a positive number")
                return 
            else:
                clustered_df = apply_kmeans(self.parent.processed_dataframe, num_clusters)
                self.parent.processed_dataframe = clustered_df
                self.parent.populate_pca_table()
                window.close()


    def retranslateUi(self, ClustersDialog):
        _translate = QtCore.QCoreApplication.translate
        ClustersDialog.setWindowTitle(_translate("ClustersDialog", "Set Number of Clusters"))
        self.NumClustersLabel.setText(_translate("ClustersDialog", "Number of Clusters:"))
        self.ElbowMethodButton.setText(_translate("ClustersDialog", "Elbow Method"))
        self.GenerateButton.setText(_translate("ClustersDialog", "Generate"))
        self.CancelButton.setText(_translate("ClustersDialog", "Cancel"))


