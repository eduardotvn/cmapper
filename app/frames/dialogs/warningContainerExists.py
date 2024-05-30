from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ContainerExistsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(533, 50)

        self.warningLabel = QtWidgets.QLabel(Dialog)
        self.warningLabel.setGeometry(QtCore.QRect(10, 10, 451, 31))
        self.warningLabel.setObjectName("warningLabel")

        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(470, 10, 61, 31))
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(Dialog.close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Warning"))
        self.warningLabel.setText(_translate("Dialog", "A postgres image is already running in this machine: \"cmapper_db\""))
        self.okButton.setText(_translate("Dialog", "Ok"))
