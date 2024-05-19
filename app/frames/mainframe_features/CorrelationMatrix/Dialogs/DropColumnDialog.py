from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DropColDialog(object):
    def __init__(self):
        self.current_dataframe = None 
        self.parent = None 

    def setupUi(self, DropColDialog):
        DropColDialog.setObjectName("DropColDialog")
        DropColDialog.resize(300, 89)

        self.colsLabel = QtWidgets.QLabel(DropColDialog)
        self.colsLabel.setGeometry(QtCore.QRect(10, 10, 71, 31))
        self.colsLabel.setObjectName("colsLabel")

        self.colsOptions = QtWidgets.QComboBox(DropColDialog)
        self.colsOptions.setGeometry(QtCore.QRect(70, 10, 171, 32))
        self.colsOptions.setObjectName("colsOptions")

        self.dropButton = QtWidgets.QPushButton(DropColDialog)
        self.dropButton.setGeometry(QtCore.QRect(10, 50, 88, 34))
        self.dropButton.setObjectName("dropButton")
        self.dropButton.clicked.connect(lambda: self.drop_column_from_dataframe(DropColDialog))

        self.cancelButton = QtWidgets.QPushButton(DropColDialog)
        self.cancelButton.setGeometry(QtCore.QRect(200, 50, 88, 34))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(DropColDialog.close)

        self.retranslateUi(DropColDialog)
        QtCore.QMetaObject.connectSlotsByName(DropColDialog)

    def set_cols_options(self, options):
        self.colsOptions.addItems(options)
    
    def drop_column_from_dataframe(self, DropColDialog):
        try: 
            col = self.colsOptions.currentText() 
            self.current_dataframe = self.current_dataframe.drop(columns=[col])
            self.parent.current_dataframe = self.current_dataframe
            self.parent.set_current_dataframe_info()
            DropColDialog.close()
        except Exception as e:
            print(e)
            DropColDialog.close()

    def retranslateUi(self, DropColDialog):
        _translate = QtCore.QCoreApplication.translate
        DropColDialog.setWindowTitle(_translate("DropColDialog", "Drop Column"))
        self.colsLabel.setText(_translate("DropColDialog", "Column"))
        self.dropButton.setText(_translate("DropColDialog", "Drop"))
        self.cancelButton.setText(_translate("DropColDialog", "Cancel"))

