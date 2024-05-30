from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WarningDocker(object):
    def setupUi(self, WarningDocker):
        WarningDocker.setObjectName("WarningDocker")
        WarningDocker.resize(443, 52)
        self.warning = QtWidgets.QLabel(WarningDocker)
        self.warning.setGeometry(QtCore.QRect(0, 10, 401, 31))
        self.warning.setObjectName("warning")
        self.ok = QtWidgets.QPushButton(WarningDocker)
        self.ok.setGeometry(QtCore.QRect(390, 10, 51, 31))
        self.ok.setObjectName("ok")
        self.ok.clicked.connect(WarningDocker.close)

        self.retranslateUi(WarningDocker)
        QtCore.QMetaObject.connectSlotsByName(WarningDocker)

    def retranslateUi(self, WarningDocker):
        _translate = QtCore.QCoreApplication.translate
        WarningDocker.setWindowTitle(_translate("WarningDocker", "Warning"))
        self.warning.setText(_translate("WarningDocker", "Warning: No cmapper docker container found. Start one in \"Create Container\".  "))
        self.ok.setText(_translate("WarningDocker", "Ok"))

