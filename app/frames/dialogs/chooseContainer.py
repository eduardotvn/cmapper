from PyQt5 import QtCore, QtGui, QtWidgets
from docker.startlocalcontainer import *
from .setContainerCredentials import Ui_setContainerCredentials
from .warningContainerExists import Ui_ContainerExistsDialog

class Ui_ChooseContainer(object):
    def __init__(self):
        self.main_window = None 
        self.containers = []

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(497, 160)

        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 491, 161))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.ChooseContainerLabel = QtWidgets.QLabel(self.groupBox)
        self.ChooseContainerLabel.setGeometry(QtCore.QRect(10, 20, 131, 31))
        self.ChooseContainerLabel.setObjectName("ChooseContainerLabel")

        self.containerCombobox = QtWidgets.QComboBox(self.groupBox)
        self.containerCombobox.setGeometry(QtCore.QRect(150, 20, 201, 32))
        self.containerCombobox.setObjectName("containerCombobox")

        self.okButton = QtWidgets.QPushButton(self.groupBox)
        self.okButton.setGeometry(QtCore.QRect(10, 120, 71, 34))
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(self.set_container)

        self.cancelButton = QtWidgets.QPushButton(self.groupBox)
        self.cancelButton.setGeometry(QtCore.QRect(400, 120, 81, 34))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(Dialog.close)

        self.CreateAndRunLabel = QtWidgets.QLabel(self.groupBox)
        self.CreateAndRunLabel.setGeometry(QtCore.QRect(10, 60, 181, 41))
        self.CreateAndRunLabel.setObjectName("CreateAndRunLabel")

        self.createAndRunButton = QtWidgets.QPushButton(self.groupBox)
        self.createAndRunButton.setGeometry(QtCore.QRect(150, 70, 201, 31))
        self.createAndRunButton.setObjectName("createAndRunButton")
        self.createAndRunButton.clicked.connect(self.create_original)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ChooseContainer"))
        self.ChooseContainerLabel.setText(_translate("Dialog", "Choose a container: "))
        self.okButton.setText(_translate("Dialog", "Ok"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.CreateAndRunLabel.setText(_translate("Dialog", "Or create and run:"))
        self.createAndRunButton.setText(_translate("Dialog", "Create Cmapper Container"))

    def set_containers_options(self, options):
        self.containerCombobox.addItems(options)
        self.containers = options

    def set_container(self):
        chosen = self.containerCombobox.currentText()
        self.main_window.current_container = chosen
        self.close()

    def create_original(self):
        if "postgrescmapper" in self.containers:
            self.Warning_Dialog = QtWidgets.QDialog()
            self.WDialog = Ui_ContainerExistsDialog()
            self.WDialog.setupUi(self.Warning_Dialog)
            self.Warning_Dialog.show()
            return
        self.Credentials_Dialog = QtWidgets.QDialog()
        self.CredDialog = Ui_setContainerCredentials()
        self.CredDialog.setupUi(self.Credentials_Dialog)
        self.Credentials_Dialog.show()
        self.CredDialog.parent = self



