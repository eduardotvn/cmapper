from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormatError(object):
    def setupUi(self, FormatError):
        FormatError.setObjectName("FormatError")
        FormatError.resize(388, 75)

        self.okButton = QtWidgets.QPushButton(FormatError)
        self.okButton.setGeometry(QtCore.QRect(307, 40, 71, 34))
        self.okButton.setObjectName("pushButton")
        self.okButton.clicked.connect(FormatError.close)

        self.label = QtWidgets.QLabel(FormatError)
        self.label.setGeometry(QtCore.QRect(10, 0, 391, 51))
        self.label.setObjectName("label")

        self.retranslateUi(FormatError)
        QtCore.QMetaObject.connectSlotsByName(FormatError)

    def retranslateUi(self, FormatError):
        _translate = QtCore.QCoreApplication.translate
        FormatError.setWindowTitle(_translate("FormatError", "Format Error"))
        self.okButton.setText(_translate("FormatError", "OK"))
        self.label.setText(_translate("FormatError", "<html><head/><body><p>Error while creating table, the chosen name is not supported.</p></body></html>"))
