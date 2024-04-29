from db.handlers.handlers import select_all_cols, filter_rows
from PyQt5 import QtCore, QtGui, QtWidgets

def load_columns(self, tableName: str):
    try:  
        cols = select_all_cols(tableName)
        self.Columns.addItems(cols)
    except Exception as e: 
        print(e)

def filter_db(self, tableName, filter_text):
    try:    
        header = select_all_cols(tableName)
        data = filter_rows(tableName, filter_text, self.Columns.currentText())

        self.DBVisualization.setRowCount(len(data))
        self.DBVisualization.setColumnCount(len(data[0]))
        self.DBVisualization.setHorizontalHeaderLabels(header)

        for row_num, row_data in enumerate(data):
            for col_num, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.DBVisualization.setItem(row_num, col_num, item)

        self.DBVisualization.resizeColumnsToContents()
        load_columns(self, tableName)
    except Exception as e:
        print(e)