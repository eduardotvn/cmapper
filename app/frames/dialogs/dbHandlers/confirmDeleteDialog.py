from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from db.connection.tableHandlers import delete_table

class Ui_ConfirmDeleteDialog(object):
    def __init__(self):
        self.chosen_table = None
        self.parent = None

    def setupUi(self, ConfirmDeleteDialog):
        ConfirmDeleteDialog.setObjectName("ConfirmDeleteDialog")
        ConfirmDeleteDialog.resize(340, 105)

        self.okButton = QtWidgets.QPushButton(ConfirmDeleteDialog)
        self.okButton.setGeometry(QtCore.QRect(0, 70, 88, 34))
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(lambda: self.try_table_deletion(ConfirmDeleteDialog))

        self.cancelButton = QtWidgets.QPushButton(ConfirmDeleteDialog)
        self.cancelButton.setGeometry(QtCore.QRect(250, 70, 88, 34))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(ConfirmDeleteDialog.close)

        self.ConfirmLabel = QtWidgets.QLabel(ConfirmDeleteDialog)
        self.ConfirmLabel.setGeometry(QtCore.QRect(30, 10, 301, 51))
        self.ConfirmLabel.setObjectName("ConfirmLabel")

        self.retranslateUi(ConfirmDeleteDialog)
        QtCore.QMetaObject.connectSlotsByName(ConfirmDeleteDialog)

    def try_table_deletion(self, ConfirmDeleteDialog):
        try:
            delete_table(self.chosen_table)
            self.parent.set_tables()
            ConfirmDeleteDialog.close()
        except Exception as e:
            QMessageBox.warning(ConfirmDeleteDialog, "Error", f"{str(e)}")

    def set_label_name(self):
        self.ConfirmLabel.setText(f"Are you sure you want to delete {self.chosen_table}? \n""This action cannot be undone.")

    def retranslateUi(self, ConfirmDeleteDialog):
        _translate = QtCore.QCoreApplication.translate
        ConfirmDeleteDialog.setWindowTitle(_translate("ConfirmDeleteDialog", "Confirm Delete"))
        self.okButton.setText(_translate("ConfirmDeleteDialog", "I am sure"))
        self.cancelButton.setText(_translate("ConfirmDeleteDialog", "Cancel"))
        self.ConfirmLabel.setText(_translate("ConfirmDeleteDialog", "Are you sure you want to delete {table_name}? \n"
"This action cannot be undone."))

