from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_currentContainer(object):
    def setupUi(self, currentContainer):
        currentContainer.setObjectName("currentContainer")
        currentContainer.resize(455, 135)
        self.groupbox = QtWidgets.QGroupBox(currentContainer)
        self.groupbox.setGeometry(QtCore.QRect(-10, 0, 471, 141))
        self.groupbox.setTitle("")
        self.groupbox.setObjectName("groupbox")
        self.containerOptions = QtWidgets.QComboBox(self.groupbox)
        self.containerOptions.setGeometry(QtCore.QRect(150, 10, 221, 32))
        self.containerOptions.setObjectName("containerOptions")
        self.CCLabel = QtWidgets.QLabel(self.groupbox)
        self.CCLabel.setGeometry(QtCore.QRect(20, 10, 121, 31))
        self.CCLabel.setObjectName("CCLabel")
        self.CCOk = QtWidgets.QPushButton(self.groupbox)
        self.CCOk.setGeometry(QtCore.QRect(20, 100, 88, 34))
        self.CCOk.setObjectName("CCOk")
        self.CCCancel = QtWidgets.QPushButton(self.groupbox)
        self.CCCancel.setGeometry(QtCore.QRect(370, 100, 88, 34))
        self.CCCancel.setObjectName("CCCancel")

        self.retranslateUi(currentContainer)
        QtCore.QMetaObject.connectSlotsByName(currentContainer)

    def retranslateUi(self, currentContainer):
        _translate = QtCore.QCoreApplication.translate
        currentContainer.setWindowTitle(_translate("currentContainer", "Choose Container"))
        self.CCLabel.setText(_translate("currentContainer", "Current Container:"))
        self.CCOk.setText(_translate("currentContainer", "Ok"))
        self.CCCancel.setText(_translate("currentContainer", "Cancel"))

