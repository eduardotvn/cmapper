from db.handlers.handlers import select_all_cols, filter_rows
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtWidgets import QMessageBox

def load_columns(self, tableName: str):
    try:  
        cols, err = select_all_cols(tableName)
        if err: 
            QMessageBox.warning(self.window, "Error", f"{str(err)}")
            return 
        self.Columns.clear()
        self.Columns.addItems(cols)
    except Exception as e: 
        QMessageBox.warning(self.window, "Error", f"{str(e)}")

def filter_db(self, tableName, filter_text):
    try:    
        header, err = select_all_cols(tableName)
        if err: 
            QMessageBox.warning(self.window, "Error", f"{str(err)}")
            return 
        data, err = filter_rows(tableName, filter_text, self.Columns.currentText())
        if err:
            QMessageBox.warning(self.window, "Error", f"{str(err)}")
            return 

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
        QMessageBox.warning(self.window, "Error", f"{str(e)}")
        
def save_data(self, dataframe):
    self.df_to_save = dataframe.copy()

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, selected_filter = QFileDialog.getSaveFileName(self.window, 'Save File', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)', options=options)

    if file_name:
        if selected_filter == 'CSV Files (*.csv)':
            if not file_name.lower().endswith('.csv'):
                file_name += '.csv'
            self.df_to_save.to_csv(file_name, index=False)
        elif selected_filter == 'Excel Files (*.xlsx)':
            if not file_name.lower().endswith('.xlsx'):
                file_name += '.xlsx'
            self.df_to_save.to_excel(file_name, index=False)
    else:
        print("No file selected")

def run_save_processed_df(self):
    if self.current_dataframe is None: 
        QMessageBox.warning(self.window, "Error", "Generate a processed database first.")
        return 
    else: 
        save_data(self, self.current_dataframe)