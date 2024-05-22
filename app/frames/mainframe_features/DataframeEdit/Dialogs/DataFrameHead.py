from PyQt5 import QtWidgets
import pandas as pd

class DataFrameDialog(QtWidgets.QDialog):
    def __init__(self, df_sample, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DataFrame Sample")
        self.setGeometry(100, 100, 800, 300)

        self.tableWidget = QtWidgets.QTableWidget()
        
        self.tableWidget.setRowCount(df_sample.shape[0])
        self.tableWidget.setColumnCount(df_sample.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(df_sample.columns)
        
        for i in range(df_sample.shape[0]):
            for j in range(df_sample.shape[1]):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(df_sample.iloc[i, j])))
        
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)