import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem

class ConfusionMatrixDialog(QDialog):
    def __init__(self, confusion_matrix):
        super().__init__()
        self.confusion_matrix = confusion_matrix
        self.setWindowTitle("Confusion Matrix")
        self.setGeometry(100, 100, 400, 400)
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.populate_confusion_matrix()

    def populate_confusion_matrix(self):
        classes = len(self.confusion_matrix)
        self.table.setRowCount(classes)
        self.table.setColumnCount(classes)
        for i in range(classes):
            for j in range(classes):
                item = QTableWidgetItem(str(self.confusion_matrix[i][j]))
                self.table.setItem(i, j, item)