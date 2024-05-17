
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from db.connection.tableHandlers import create_table
import re 

class Ui_CreateTableDialog(object):
    def __init__(self):
        self.columns = []
        self.table_name = None 
        self.options = ["text", "byte", "timestamp", "integer", "float", "boolean"]
        self.parent = None

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
        self.cancelButton.clicked.connect(CreateTableDialog.close)
        
        self.addColumnButton = QtWidgets.QPushButton(CreateTableDialog)
        self.addColumnButton.setGeometry(QtCore.QRect(10, 70, 88, 34))
        self.addColumnButton.setObjectName("addColumnButton")
        self.addColumnButton.clicked.connect(lambda: self.add_column(CreateTableDialog))        

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
        self.table_name_dialog()

    def gather_data(self, CreateTableDialog):
        try:
            if self.is_valid_postgres_identifier(self.columnNameInput.text()):
                col_name = self.columnNameInput.text()
                col_type = self.columnType.currentText()
                return [col_name, col_type]
            else: 
                QMessageBox.warning(CreateTableDialog, "Invalid Column Name", f"'{self.columnNameInput.text()}' is not a valid PostgreSQL column identifier.")
                return None 
        except Exception as e: 
            print(e)
            return

    def add_column(self, CreateTableDialog):
        try: 
            if self.table_name == None:
                if self.is_valid_postgres_identifier(self.columnNameInput.text()):
                    self.table_name = self.columnNameInput.text()
                    self.columnNameInput.clear()
                    self.columns_dialog(CreateTableDialog)
                    return 
                else: 
                    QMessageBox.warning(CreateTableDialog, "Invalid Table Name", f"'{self.columnNameInput.text()}' is not a valid PostgreSQL table name.")
                    self.columnNameInput.clear()
                    return
            col = self.gather_data(CreateTableDialog)
            if col != None:
                self.columns.append(col)
                self.columnNameInput.clear()
            else: 
                self.columnNameInput.clear()
                return 
        except Exception as e:
            print(e)
            return 

    def create_table_action(self, CreateTableDialog):
        try:
            if len(self.columns) > 0:
                create_table(self.table_name, self.columns)
                self.parent.set_tables()
                CreateTableDialog.close()
            else:
                QMessageBox.warning(CreateTableDialog, "Invalid Schema", "Add at least one column")
                return
        except Exception as e:
            QMessageBox.critical(CreateTableDialog, "Error", f"An error occurred: {str(e)}")
            CreateTableDialog.close()

    def set_types_options(self, options):
        self.columnType.addItems(options)

    def table_name_dialog(self):
        self.columnType.hide()
        self.columnNameLabel.setText("Table Name:")
        self.createButton.hide()
    
    def columns_dialog(self,CreateTableDialog):
        self.columnType.show()
        self.columnNameLabel.setText("Column Name:")
        self.createButton.show()
        QMessageBox.warning(CreateTableDialog, "Warning" ,"A serial primary key 'id' will be automatically added.")
        

    def is_valid_postgres_identifier(self, name):
        if name.upper() in reserved_keywords:
            return False
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
            return False
        if len(name) > 63:
            return False
        return True

    def retranslateUi(self, CreateTableDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateTableDialog.setWindowTitle(_translate("CreateTableDialog", "Create Table"))
        self.createButton.setText(_translate("CreateTableDialog", "Create"))
        self.cancelButton.setText(_translate("CreateTableDialog", "Cancel"))
        self.columnNameLabel.setText(_translate("CreateTableDialog", "Column Name:"))
        self.addColumnButton.setText(_translate("CreateTableDialog", "Add Column"))

reserved_keywords = {
    "ALL", "ANALYSE", "ANALYZE", "AND", "ANY", "ARRAY", "AS", "ASC", "ASYMMETRIC",
    "AUTHORIZATION", "BINARY", "BOTH", "CASE", "CAST", "CHECK", "COLLATE", "COLUMN",
    "CONSTRAINT", "CREATE", "CROSS", "CURRENT_DATE", "CURRENT_ROLE", "CURRENT_TIME",
    "CURRENT_TIMESTAMP", "CURRENT_USER", "DEFAULT", "DEFERRABLE", "DESC", "DISTINCT",
    "DO", "ELSE", "END", "EXCEPT", "FALSE", "FOR", "FOREIGN", "FREEZE", "FROM",
    "FULL", "GRANT", "GROUP", "HAVING", "ILIKE", "IN", "INITIALLY", "INNER", "INTERSECT",
    "INTO", "IS", "ISNULL", "JOIN", "LATERAL", "LEADING", "LEFT", "LIKE", "LIMIT", "LOCALTIME",
    "LOCALTIMESTAMP", "NATURAL", "NOT", "NOTNULL", "NULL", "OFFSET", "ON", "ONLY", "OR",
    "ORDER", "OUTER", "OVERLAPS", "PLACING", "PRIMARY", "REFERENCES", "RETURNING",
    "RIGHT", "SELECT", "SESSION_USER", "SIMILAR", "SOME", "SYMMETRIC", "TABLE", "THEN",
    "TO", "TRAILING", "TRUE", "UNION", "UNIQUE", "USER", "USING", "VERBOSE", "WHEN", "WHERE"
}
