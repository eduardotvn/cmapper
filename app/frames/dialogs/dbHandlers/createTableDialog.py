
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateTableDialog(object):
    def __init__(self):
        self.rows = []
        self.table_name = None 
        self.options = ["text", "byte", "timestamp", "integer", "float", "boolean"]

    def setupUi(self, CreateTableDialog):
        CreateTableDialog.setObjectName("CreateTableDialog")
        CreateTableDialog.resize(441, 107)

        self.createButton = QtWidgets.QPushButton(CreateTableDialog)
        self.createButton.setGeometry(QtCore.QRect(240, 70, 88, 34))
        self.createButton.setObjectName("createButton")
        self.createButton.clicked.connect(lambda: self.create_table_action(CreateTableDialog))

        self.cancelButton = QtWidgets.QPushButton(CreateTableDialog)
        self.cancelButton.setGeometry(QtCore.QRect(340, 70, 88, 34))
        self.cancelButton.setObjectName("cancelButton")
        
        self.addColumnButton = QtWidgets.QPushButton(CreateTableDialog)
        self.addColumnButton.setGeometry(QtCore.QRect(10, 70, 88, 34))
        self.addColumnButton.setObjectName("addColumnButton")
        self.addColumnButton.clicked.connect(self.add_column)        

        self.columnNameLabel = QtWidgets.QLabel(CreateTableDialog)
        self.columnNameLabel.setGeometry(QtCore.QRect(10, 20, 101, 31))
        self.columnNameLabel.setObjectName("columnNameLabel")

        self.columnNameInput = QtWidgets.QLineEdit(CreateTableDialog)
        self.columnNameInput.setGeometry(QtCore.QRect(110, 20, 201, 32))
        self.columnNameInput.setObjectName("columnNameInput")

        self.columnType = QtWidgets.QComboBox(CreateTableDialog)
        self.columnType.setGeometry(QtCore.QRect(320, 20, 111, 32))
        self.columnType.setObjectName("columnType")

        self.retranslateUi(CreateTableDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateTableDialog)
        self.set_types_options(self.options)

    def gather_data(self):
        try:
            row_name = self.columnNameInput.text()
            row_type = self.columnType.currentText()
            return [row_name, row_type]
        except Exception as e: 
            print(e)
            return

    def add_column(self):
        try: 
            col = self.gather_data()
            self.rows.append(col)
            self.columnNameInput.clear()
        except Exception as e:
            print(e)
            return 

    def create_table_action(self, CreateTableDialog):
        try:
            CreateTableDialog.close()
        except Exception as e:
            print(e)
            CreateTableDialog.close()

    def set_types_options(self, options):
        self.columnType.addItems(options)

    def retranslateUi(self, CreateTableDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateTableDialog.setWindowTitle(_translate("CreateTableDialog", "Create Table"))
        self.createButton.setText(_translate("CreateTableDialog", "Create"))
        self.cancelButton.setText(_translate("CreateTableDialog", "Cancel"))
        self.columnNameLabel.setText(_translate("CreateTableDialog", "Column Name"))
        self.addColumnButton.setText(_translate("CreateTableDialog", "Add Column"))

