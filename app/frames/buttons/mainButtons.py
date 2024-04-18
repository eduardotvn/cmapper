from db.handlers.handlers import select_all_rows
from PyQt5 import QtCore, QtGui, QtWidgets
from .mainFuncs import load_columns

def refresh_db_visualization(self, tableName):
    data, header = select_all_rows(tableName)

    self.DBVisualization.setRowCount(len(data))
    self.DBVisualization.setColumnCount(len(data[0]))
    self.DBVisualization.setHorizontalHeaderLabels(header)

    for row_num, row_data in enumerate(data):
        for col_num, value in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(str(value))
            self.DBVisualization.setItem(row_num, col_num, item)

    self.DBVisualization.resizeColumnsToContents()
    load_columns(self, tableName)

