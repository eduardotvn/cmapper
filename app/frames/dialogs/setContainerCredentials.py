

from PyQt5 import QtCore, QtGui, QtWidgets
from docker.startlocalcontainer import start_postgres_container

class Ui_setContainerCredentials(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(454, 124)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(-10, 0, 471, 131))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.usernameLabel = QtWidgets.QLabel(self.groupBox)
        self.usernameLabel.setGeometry(QtCore.QRect(30, 10, 71, 31))
        self.usernameLabel.setObjectName("usernameLabel")

        self.passwordLabel = QtWidgets.QLabel(self.groupBox)
        self.passwordLabel.setGeometry(QtCore.QRect(30, 70, 81, 31))
        self.passwordLabel.setObjectName("passwordLabel")

        self.inputUsername = QtWidgets.QLineEdit(self.groupBox)
        self.inputUsername.setGeometry(QtCore.QRect(120, 10, 221, 31))
        self.inputUsername.setObjectName("inputUsername")

        self.inputPassword = QtWidgets.QLineEdit(self.groupBox)
        self.inputPassword.setGeometry(QtCore.QRect(120, 70, 221, 31))
        self.inputPassword.setObjectName("inputPassword")

        self.createButton = QtWidgets.QPushButton(self.groupBox)
        self.createButton.setGeometry(QtCore.QRect(360, 70, 88, 34))
        self.createButton.setObjectName("createButton")
        self.createButton.clicked.connect(self.start_container)

        self.cancelButton = QtWidgets.QPushButton(self.groupBox)
        self.cancelButton.setGeometry(QtCore.QRect(360, 10, 88, 34))
        self.cancelButton.setObjectName("cancelButton")
        self.createButton.clicked.connect(Dialog.close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Set Credentials"))
        self.usernameLabel.setText(_translate("Dialog", "Username"))
        self.passwordLabel.setText(_translate("Dialog", "Password"))
        self.createButton.setText(_translate("Dialog", "Create"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))

    def start_container(self):
        try:
            success, error = start_postgres_container("postgrescmapper", self.inputUsername.text(), self.inputPassword.text())
            if not success:
                raise Exception(error)  
        except Exception as e:
            print(f"Error starting container: {e}")
            raise e
                
