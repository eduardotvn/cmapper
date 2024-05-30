from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from db.handlers.handlers import select_all_cols_and_types, find_primary_key_column, update_table

class Ui_UpdateDataDialog(object):
    def __init__(self):
        self.chosen_table = None
        self.column_options = []
        self.columns_and_types = []
        self.parent = None 
 
    def setupUi(self, UpdateDataDialog):
        UpdateDataDialog.setObjectName("UpdateDataDialog")
        UpdateDataDialog.resize(227, 184)

        self.PrimaryKeyLabel = QtWidgets.QLabel(UpdateDataDialog)
        self.PrimaryKeyLabel.setGeometry(QtCore.QRect(10, 10, 111, 31))
        self.PrimaryKeyLabel.setObjectName("PrimaryKeyLabel")

        self.okButton = QtWidgets.QPushButton(UpdateDataDialog)
        self.okButton.setGeometry(QtCore.QRect(0, 150, 88, 34))
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(lambda: self.update_data(UpdateDataDialog))

        self.cancelButton = QtWidgets.QPushButton(UpdateDataDialog)
        self.cancelButton.setGeometry(QtCore.QRect(140, 150, 88, 34))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(UpdateDataDialog.close)

        self.PrimaryKeyInput = QtWidgets.QLineEdit(UpdateDataDialog)
        self.PrimaryKeyInput.setGeometry(QtCore.QRect(90, 10, 131, 32))
        self.PrimaryKeyInput.setObjectName("PrimaryKeyInput")

        self.ColumnsOptions = QtWidgets.QComboBox(UpdateDataDialog)
        self.ColumnsOptions.setGeometry(QtCore.QRect(90, 50, 131, 32))
        self.ColumnsOptions.setObjectName("ColumnsOptions")

        self.ValueInput = QtWidgets.QLineEdit(UpdateDataDialog)
        self.ValueInput.setGeometry(QtCore.QRect(90, 90, 131, 32))
        self.ValueInput.setObjectName("ValueInput")

        self.ColumnLabel = QtWidgets.QLabel(UpdateDataDialog)
        self.ColumnLabel.setGeometry(QtCore.QRect(10, 50, 81, 31))
        self.ColumnLabel.setObjectName("ColumnLabel")

        self.ValueLabel = QtWidgets.QLabel(UpdateDataDialog)
        self.ValueLabel.setGeometry(QtCore.QRect(10, 90, 61, 31))
        self.ValueLabel.setObjectName("ValueLabel")

        self.retranslateUi(UpdateDataDialog)
        QtCore.QMetaObject.connectSlotsByName(UpdateDataDialog)
        self.set_column_options(UpdateDataDialog)

    def set_column_options(self, UpdateDataDialog):
        try:
            cols_and_types, err = select_all_cols_and_types(self.chosen_table)
            if err: 
                QMessageBox.warning(self.window, "Error", f"{str(err)}")
                return 
            pkey = find_primary_key_column(self.chosen_table)[0]
            self.column_options = [cols[0] for cols in cols_and_types]
            if pkey != None: 
                self.column_options.remove(pkey)
            self.ColumnsOptions.addItems(self.column_options)
        except Exception as e:
            QMessageBox.warning(UpdateDataDialog, "Error setting options", f"{str(e)}")

    def update_data(self, UpdateDataDialog):
        try:
            pkey = self.PrimaryKeyInput.text()
            col = self.ColumnsOptions.currentText()
            value = self.ValueInput.text()
            success,_ = update_table(self.chosen_table, col, value, pkey)
            if success:
                QMessageBox.warning(UpdateDataDialog, "Success!", "The row was succesfuly updated.")
            if self.parent != None:
                self.parent.run_refresh()
            UpdateDataDialog.close()
        except Exception as e:
            QMessageBox.warning(UpdateDataDialog, "Error", f"{str(e)}")
            UpdateDataDialog.close()

    def retranslateUi(self, UpdateDataDialog):
        _translate = QtCore.QCoreApplication.translate
        UpdateDataDialog.setWindowTitle(_translate("UpdateDataDialog", "Update Data"))
        self.PrimaryKeyLabel.setText(_translate("UpdateDataDialog", "Primary Key:"))
        self.okButton.setText(_translate("UpdateDataDialog", "Update"))
        self.cancelButton.setText(_translate("UpdateDataDialog", "Cancel"))
        self.ColumnLabel.setText(_translate("UpdateDataDialog", "Column:"))
        self.ValueLabel.setText(_translate("UpdateDataDialog", "Value:"))
