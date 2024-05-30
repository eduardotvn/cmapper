
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from db.fileHandling.csvIntoPostgres import turn_column_into_primary_key
from db.handlers.handlers import create_new_pkey

class Ui_PrimaryKeyConfirm(object):
    def __init__(self):
        self.found_cols = []
        self.chosen_table = None         

    def setupUi(self, PrimaryKeyConfirm):
        PrimaryKeyConfirm.setObjectName("PrimaryKeyConfirm")
        PrimaryKeyConfirm.resize(429, 91)

        self.yesButton = QtWidgets.QPushButton(PrimaryKeyConfirm)
        self.yesButton.setGeometry(QtCore.QRect(10, 50, 88, 34))
        self.yesButton.setObjectName("yesButton")
        self.yesButton.clicked.connect(lambda: self.choose_col(PrimaryKeyConfirm))

        self.autoButton = QtWidgets.QPushButton(PrimaryKeyConfirm)
        self.autoButton.setGeometry(QtCore.QRect(105, 50, 88, 34))
        self.autoButton.setObjectName("autoButton")
        self.autoButton.setToolTip("Creates a new serial primary key column 'pkey'")
        self.autoButton.clicked.connect(lambda: self.gen_pkey(PrimaryKeyConfirm))

        self.searchAgainButton = QtWidgets.QPushButton(PrimaryKeyConfirm)
        self.searchAgainButton.setGeometry(QtCore.QRect(327, 50, 91, 34))
        self.searchAgainButton.setObjectName("searchAgainButton")
        self.searchAgainButton.clicked.connect(lambda: self.next_col(PrimaryKeyConfirm))

        self.ConfirmKeyLabel = QtWidgets.QLabel(PrimaryKeyConfirm)
        self.ConfirmKeyLabel.setGeometry(QtCore.QRect(10, 9, 411, 31))
        self.ConfirmKeyLabel.setObjectName("ConfirmKeyLabel")

        self.retranslateUi(PrimaryKeyConfirm)
        QtCore.QMetaObject.connectSlotsByName(PrimaryKeyConfirm)

    def choose_col(self, PrimaryKeyConfirm):
        try:
            print("col :", self.found_cols[0])
            if turn_column_into_primary_key(self.chosen_table, self.found_cols[0]):
                print("Succesful")
            PrimaryKeyConfirm.close()
        except Exception as e: 
            print(e)

    def gen_pkey(self, PrimaryKeyConfirm):
        try: 
            success, err = create_new_pkey(self.chosen_table)
            if success:
                print("Succesfuly created pkey")
            else: 
                QMessageBox.warning(self.window, "Error", f"{str(err)}")
            PrimaryKeyConfirm.close()
        except Exception as e:
            print(e)
            PrimaryKeyConfirm.close()

    def next_col(self, PrimaryKeyConfirm):
        self.found_cols.pop(0)
        if len(self.found_cols) == 0: 
            PrimaryKeyConfirm.close()
        else: 
            self.set_col_label(self.found_cols[0])

    def set_col_label(self, col):
        self.ConfirmKeyLabel.setText(f"Turn {col} into primary key? ")

    def retranslateUi(self, PrimaryKeyConfirm):
        _translate = QtCore.QCoreApplication.translate
        PrimaryKeyConfirm.setWindowTitle(_translate("PrimaryKeyConfirm", "Confirm Primary Key"))
        self.yesButton.setText(_translate("PrimaryKeyConfirm", "Yes"))
        self.searchAgainButton.setText(_translate("PrimaryKeyConfirm", "Search Again"))
        self.ConfirmKeyLabel.setText(_translate("PrimaryKeyConfirm", "Turn {Column Name} into primary key? "))
        self.autoButton.setText(_translate("AutoButton", "Generate"))