from db.handlers.handlers import select_all_rows
from PyQt5 import QtCore, QtGui, QtWidgets
from .mainFuncs import load_columns
from frames.dialogs.createDbDialog import Ui_CreateDatabaseFromFile
from frames.dialogs.chooseContainer import Ui_ChooseContainer

def refresh_db_visualization(self, tableName):

    if self.current_container == None: 
        run_choose_container_dialog(self)

    if self.current_container == None: 
        return 

    data, header = select_all_rows(tableName)

    if len(data) == 0:
        self.DBVisualization.setRowCount(0)
        self.DBVisualization.setColumnCount(0)
        self.DBVisualization.setHorizontalHeaderLabels([""])
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


def run_creation_dialog(self):
    self.Creatrion_Dialog = QtWidgets.QDialog()
    self.CDialog = Ui_CreateDatabaseFromFile()
    self.CDialog.setupUi(self.Creatrion_Dialog)
    self.CDialog.main_window = self
    self.Creatrion_Dialog.show()

def run_choose_container_dialog(self):
    self.Choose_Container_Dialog = QtWidgets.QDialog()
    self.Choose_Container = Ui_ChooseContainer()
    self.Choose_Container.setupUi(self.Choose_Container_Dialog)
    self.Choose_Container.main_window = self
    self.Choose_Container_Dialog.show()
    self.Choose_Container.set_containers_options(self.found_containers)