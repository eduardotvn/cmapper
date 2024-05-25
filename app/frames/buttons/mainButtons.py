from db.handlers.handlers import select_all_rows, select_all_cols_and_types, find_primary_key_column
from PyQt5 import QtCore, QtGui, QtWidgets
from .mainFuncs import load_columns
from frames.dialogs.createDbDialog import Ui_CreateDatabaseFromFile
from frames.dialogs.chooseContainer import Ui_ChooseContainer
from frames.dialogs.formatErrorDialog import Ui_FormatError
from frames.dialogs.dbHandlers.inputDataDialog import Ui_InputData
from frames.dialogs.dbHandlers.deleteRowDialog import Ui_DeleteDialog
from frames.dialogs.dbHandlers.createTableDialog import Ui_CreateTableDialog
from frames.dialogs.dbHandlers.confirmDeleteDialog import Ui_ConfirmDeleteDialog
from frames.dialogs.dbHandlers.updateDataDialog import Ui_UpdateDataDialog
from frames.dialogs.aboutCmapper import Ui_AboutDialog

def refresh_db_visualization(self, tableName):

    if self.current_container == None: 
        run_choose_container_dialog(self)
    if self.current_container == None: 
        return 
    if tableName == None or tableName == "":
        return 

    data, header = select_all_rows(tableName)

    if len(data) == 0:
        self.DBVisualization.clear()
        self.DBVisualization.setRowCount(0)
        self.DBVisualization.setColumnCount(0)
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


def run_db_insertion_dialog(self):
    try:
        chosen_table = self.current_table

        self.InputData_Dialog = QtWidgets.QDialog()
        self.InputData = Ui_InputData()
        self.InputData.setupUi(self.InputData_Dialog)
        self.InputData_Dialog.show()

        cols_info = select_all_cols_and_types(chosen_table)
        pkey = find_primary_key_column(chosen_table)
        if len(pkey) > 0:
            for col in cols_info:
                if col[0] == pkey[0]:
                    cols_info.remove(col)
        self.InputData.cols_info = cols_info
        self.InputData.chosen_table = chosen_table
        self.InputData.set_column_name(cols_info[0][0])
    except Exception as e: 
        print(e)
        return

def run_creation_dialog(self):
    self.Creatrion_Dialog = QtWidgets.QDialog()
    self.CDialog = Ui_CreateDatabaseFromFile()
    self.CDialog.setupUi(self.Creatrion_Dialog)
    self.CDialog.main_window = self
    self.Creatrion_Dialog.show()

def run_about_dialog(self):
    self.About_Dialog = QtWidgets.QDialog()
    self.AboutDialog = Ui_AboutDialog()
    self.AboutDialog.setupUi(self.About_Dialog)
    self.About_Dialog.show()

def run_choose_container_dialog(self):
    self.Choose_Container_Dialog = QtWidgets.QDialog()
    self.Choose_Container = Ui_ChooseContainer()
    self.Choose_Container.setupUi(self.Choose_Container_Dialog)
    self.Choose_Container.main_window = self
    self.Choose_Container_Dialog.show()
    self.Choose_Container.set_containers_options(self.found_containers)

def run_format_error_dialog(self):
    self.FormatError_Dialog = QtWidgets.QDialog()
    self.FEDialog = Ui_FormatError()
    self.FEDialog.setupUi(self.FormatError_Dialog)
    self.FormatError_Dialog.show()

def run_delete_row_dialog(self):
    self.DeleteRow_Dialog = QtWidgets.QDialog()
    self.DRDialog = Ui_DeleteDialog()
    self.DRDialog.setupUi(self.DeleteRow_Dialog)
    self.DeleteRow_Dialog.show()
    self.DRDialog.chosen_table = self.current_table

def run_update_row_dialog(self):
    self.UpdateData_Dialog = QtWidgets.QDialog()
    self.UDDialog = Ui_UpdateDataDialog()
    self.UDDialog.chosen_table = self.current_table
    self.UDDialog.parent = self
    self.UDDialog.setupUi(self.UpdateData_Dialog)
    self.UpdateData_Dialog.show()

def run_create_table_dialog(self):
    self.CreateTable_Dialog = QtWidgets.QDialog()
    self.CTDialog = Ui_CreateTableDialog()
    self.CTDialog.setupUi(self.CreateTable_Dialog)
    self.CreateTable_Dialog.show()
    self.CTDialog.parent = self 

def run_delete_db_dialog(self):
    self.ConfirmDeleteDialog = QtWidgets.QDialog()
    self.CDDialog = Ui_ConfirmDeleteDialog()
    self.CDDialog.setupUi(self.ConfirmDeleteDialog)
    self.ConfirmDeleteDialog.show()
    self.CDDialog.chosen_table = self.current_table
    self.CDDialog.set_label_name()
    self.CDDialog.parent = self 