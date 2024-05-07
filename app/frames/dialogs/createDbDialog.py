from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from db.fileHandling.csvIntoPostgres import try_table_creation

class Ui_CreateDatabaseFromFile(object):
    def __init__(self):
        self.chosen_file = None 

    def setupUi(self, CreateDatabaseFromFile):
        CreateDatabaseFromFile.setObjectName("CreateDatabaseFromFile")
        CreateDatabaseFromFile.resize(400, 168)

        self.DBNameInput = QtWidgets.QLineEdit(CreateDatabaseFromFile)
        self.DBNameInput.setGeometry(QtCore.QRect(60, 10, 301, 41))
        self.DBNameInput.setObjectName("DBNameInput")

        self.FileName = QtWidgets.QLabel(CreateDatabaseFromFile)
        self.FileName.setGeometry(QtCore.QRect(10, 10, 51, 41))
        self.FileName.setObjectName("FileName")

        self.FileURL = QtWidgets.QLabel(CreateDatabaseFromFile)
        self.FileURL.setGeometry(QtCore.QRect(20, 70, 31, 41))
        self.FileURL.setObjectName("FileURL")

        self.SearchFileButton = QtWidgets.QPushButton(CreateDatabaseFromFile)
        self.SearchFileButton.setGeometry(QtCore.QRect(60, 70, 81, 41))
        self.SearchFileButton.setObjectName("SearchFileButton")
        self.SearchFileButton.clicked.connect(self.open_file_dialog)

        self.OkButton = QtWidgets.QPushButton(CreateDatabaseFromFile)
        self.OkButton.setGeometry(QtCore.QRect(210, 130, 88, 34))
        self.OkButton.setObjectName("OkButton")
        self.OkButton.clicked.connect(lambda: self.table_creation(CreateDatabaseFromFile))

        self.CancelButton = QtWidgets.QPushButton(CreateDatabaseFromFile)
        self.CancelButton.setGeometry(QtCore.QRect(310, 130, 88, 34))
        self.CancelButton.setObjectName("CancelButton")
        self.CancelButton.clicked.connect(CreateDatabaseFromFile.close)

        self.URLPath = QtWidgets.QLabel(CreateDatabaseFromFile)
        self.URLPath.setGeometry(QtCore.QRect(170, 70, 221, 41))
        self.URLPath.setText("")
        self.URLPath.setObjectName("URLPath")

        self.retranslateUi(CreateDatabaseFromFile)
        QtCore.QMetaObject.connectSlotsByName(CreateDatabaseFromFile)

    def open_file_dialog(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.setNameFilter("CSV Files (*.csv)")
        self.file_dialog.setViewMode(QFileDialog.Detail)
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)
        if self.file_dialog.exec_():
            selected_files = self.file_dialog.selectedFiles()
            if selected_files:
                selected_file_path = selected_files[0]
                print("Selected CSV file:", selected_file_path)
                self.chosen_file = selected_file_path
                self.URLPath.setText(f'{selected_file_path}')
    
    def get_db_name(self):
        current_text = self.DBNameInput.text()
        if current_text.strip() == "":
            return False, ""
        elif current_text.strip().isdigit():
            return False, ""
        else: 
            current_text = ''.join([c if c !=' ' else '_' for c in current_text.strip()])
            return True, current_text
    
    def table_creation(self, CreateDatabaseFromFile):
        from frames.buttons.mainButtons import run_format_error_dialog
        con, dbname = self.get_db_name()
        if dbname in self.main_window.found_tables or dbname == "":
            run_format_error_dialog(self)
            return 
        if not con: 
            return 
        if self.chosen_file is not None:
            try_table_creation(dbname, self.chosen_file)
            self.chosen_file = None
            self.main_window.run_refresh()
            self.main_window.set_tables()
            CreateDatabaseFromFile.close()
    
    def retranslateUi(self, CreateDatabaseFromFile):
        _translate = QtCore.QCoreApplication.translate
        CreateDatabaseFromFile.setWindowTitle(_translate("CreateDatabaseFromFile", "Dialog"))
        self.FileName.setText(_translate("CreateDatabaseFromFile", "Name:"))
        self.FileURL.setText(_translate("CreateDatabaseFromFile", "File: "))
        self.SearchFileButton.setText(_translate("CreateDatabaseFromFile", "Search..."))
        self.OkButton.setText(_translate("CreateDatabaseFromFile", "Ok"))
        self.CancelButton.setText(_translate("CreateDatabaseFromFile", "Cancel"))
    
