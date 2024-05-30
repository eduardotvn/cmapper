from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from db.handlers.handlers import delete_row

class Ui_DeleteDialog(object):
    def __init__(self):
        self.chosen_table = None 
    def setupUi(self, DeleteDialog):
        DeleteDialog.setObjectName("DeleteDialog")
        DeleteDialog.resize(451, 97)

        self.OkButton = QtWidgets.QPushButton(DeleteDialog)
        self.OkButton.setGeometry(QtCore.QRect(0, 60, 88, 34))
        self.OkButton.setObjectName("OkButton")
        self.OkButton.clicked.connect(lambda: self.delete_row_action(DeleteDialog))

        self.CancelButton = QtWidgets.QPushButton(DeleteDialog)
        self.CancelButton.setGeometry(QtCore.QRect(360, 60, 88, 34))
        self.CancelButton.setObjectName("CancelButton")
        self.CancelButton.clicked.connect(DeleteDialog.close)

        self.PKeyLabel = QtWidgets.QLabel(DeleteDialog)
        self.PKeyLabel.setGeometry(QtCore.QRect(10, 10, 211, 51))
        self.PKeyLabel.setObjectName("PKeyLabel")
        
        self.PKeyInput = QtWidgets.QLineEdit(DeleteDialog)
        self.PKeyInput.setGeometry(QtCore.QRect(220, 20, 221, 31))
        self.PKeyInput.setObjectName("PKeyInput")

        self.retranslateUi(DeleteDialog)
        QtCore.QMetaObject.connectSlotsByName(DeleteDialog)

    def delete_row_action(self, DeleteDialog):
        try:
            key = self.PKeyInput.text()
            success, err = delete_row(self.chosen_table, key)
            if err:
                QMessageBox.warning(self.window, "Error", f"{str(err)}")
            DeleteDialog.close()
        except Exception as e: 
            print(e)
            DeleteDialog.close()

    def retranslateUi(self, DeleteDialog):
        _translate = QtCore.QCoreApplication.translate
        DeleteDialog.setWindowTitle(_translate("DeleteDialog", "Delete Row"))
        self.OkButton.setText(_translate("DeleteDialog", "Delete"))
        self.CancelButton.setText(_translate("DeleteDialog", "Cancel"))
        self.PKeyLabel.setText(_translate("DeleteDialog", "Primary Key of row to be deleted:"))

