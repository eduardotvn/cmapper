from PyQt5 import QtCore, QtGui, QtWidgets
from docker.startlocalcontainer import *
from .warningContainerExists import Ui_ContainerExistsDialog
import os 

class Ui_CreateContainer(object):
    def __init__(self):
        self.parent = None 

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(230, 250)

        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 230, 250))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.InfoLabel = QtWidgets.QLabel(self.groupBox)
        self.InfoLabel.setGeometry(QtCore.QRect(15, 0, 240, 200))
        self.InfoLabel.setText(
f"""A PostGres Image will be created
with the following information:

DBNAME: {os.getenv('DBNAME')}
USERNAME: {os.getenv('USERNAME')}
PASSWORD: {os.getenv('PASSWORD')}
HOST: {os.getenv('HOST')}
PORT: {os.getenv('PORT')}
   """)

        self.cancelButton = QtWidgets.QPushButton(self.groupBox)
        self.cancelButton.setGeometry(QtCore.QRect(130, 210, 81, 34))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(Dialog.close)

        self.createAndRunButton = QtWidgets.QPushButton(self.groupBox)
        self.createAndRunButton.setGeometry(QtCore.QRect(10, 170, 201, 31))
        self.createAndRunButton.setObjectName("createAndRunButton")
        self.createAndRunButton.clicked.connect(lambda: self.create_original(Dialog))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Create Container"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.createAndRunButton.setText(_translate("Dialog", "Create Cmapper Container"))

    def create_original(self, dialog):
        if "cmapper_db" in self.containers:
            self.Warning_Dialog = QtWidgets.QDialog()
            self.WDialog = Ui_ContainerExistsDialog()
            self.WDialog.setupUi(self.Warning_Dialog)
            self.Warning_Dialog.show()
            return
        if start_postgres_container():
            self.parent.current_container = "cmapper_db"
            dialog.close()
        



