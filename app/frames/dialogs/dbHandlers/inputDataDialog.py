from PyQt5 import QtCore, QtGui, QtWidgets
from db.handlers.handlers import insert_table
from PyQt5.QtWidgets import QMessageBox

class Ui_InputData(object):
    def __init__(self):
        self.cols_info = []
        self.chosen_table = None
        self.insertion_schema = []

    def setupUi(self, InputData):
        InputData.setObjectName("InputData")
        InputData.resize(504, 98)

        self.okButton = QtWidgets.QPushButton(InputData)
        self.okButton.setGeometry(QtCore.QRect(410, 60, 88, 34))
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(lambda : self.gather_data(InputData))

        self.cancelButton = QtWidgets.QPushButton(InputData)
        self.cancelButton.setGeometry(QtCore.QRect(0, 60, 88, 34))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(InputData.close)

        self.dataInput = QtWidgets.QLineEdit(InputData)
        self.dataInput.setGeometry(QtCore.QRect(160, 10, 341, 41))
        self.dataInput.setObjectName("dataInput")

        self.column_name = QtWidgets.QLabel(InputData)
        self.column_name.setGeometry(QtCore.QRect(10, 10, 141, 41))
        self.column_name.setObjectName("column_name")

        self.retranslateUi(InputData)
        QtCore.QMetaObject.connectSlotsByName(InputData)

    def set_column_name(self, text):
        self.column_name.setText(text)
    
    def set_current_type(self, colType):
        self.column_type = colType 

    def proccess_input(self, input, colType):
        if colType == "text" or colType == "date":
            return f"'{input}'"
        else:
            return input

    def gather_data(self, InputData):
        try:
            data = self.proccess_input(self.dataInput.text(), self.cols_info[0][1])
            self.insertion_schema.append(data)
            self.dataInput.clear()
            self.cols_info.pop(0)
            if len(self.cols_info) > 0: 
                self.set_column_name(f'{self.cols_info[0][0]}')
            else: 
                _, err = insert_table(self.chosen_table, self.insertion_schema)
                if err is not None:
                    QMessageBox.warning(self.window, "Error", f"{str(err)}")
                self.refresh_db_visualization()
                InputData.close()
        except Exception as err: 
            QMessageBox.warning(self.window, "Error", f"{str(err)}")
            InputData.close()

    def retranslateUi(self, InputData):
        _translate = QtCore.QCoreApplication.translate
        InputData.setWindowTitle(_translate("InputData", "Input Data"))
        self.okButton.setText(_translate("InputData", "Next"))
        self.cancelButton.setText(_translate("InputData", "Cancel"))
        self.column_name.setText(_translate("InputData", "Column Name"))

