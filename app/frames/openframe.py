import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QStatusBar
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from docker.findcontainers import find_running_postgres_containers
from .mainframe import Ui_MainWindow
from .dialogs.warningDocker import Ui_WarningDocker
import time 

class OpenFrame(QMainWindow):
    def __new__(cls):
        cls.width = 1024
        cls.height = 576
        return super(OpenFrame, cls).__new__(cls)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cmapper") 

        self.first = None 
        self.container_list = []

        pixmap = QPixmap("app/assets/images/beautiful-shot-colorful-tulips-field-sunny-day.jpg").scaled(1024, 576)

        self.background_img = QLabel(self)
        self.background_img.setPixmap(pixmap)
        self.background_img.setGeometry(0, 0, OpenFrame.width, OpenFrame.height)

        self.setGeometry(0, 0, OpenFrame.width, OpenFrame.height)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("background-color: white;") 
        self.status_bar.showMessage("Loading...")

    def load_mainframe(self):
        try:
            self.MainWindow = QtWidgets.QMainWindow()
            self.main = Ui_MainWindow()
            self.main.setupUi(self.MainWindow)
            self.MainWindow.show()
            if len(find_running_postgres_containers()) == 0:
                self.warningDialog = QtWidgets.QDialog()
                self.warning = Ui_WarningDocker()
                self.warning.setupUi(self.warningDialog)
                self.warningDialog.show()
            self.main.set_container_data(find_running_postgres_containers())
            self.close()
        except Exception as e:
            print("Error loading MainFrame:", e)

