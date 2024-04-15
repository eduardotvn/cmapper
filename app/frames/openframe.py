import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QStatusBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from .mainframe import MainFrame
import time 

class OpenFrame(QMainWindow):
    def __new__(cls):
        cls.width = 1024
        cls.height = 576
        return super(OpenFrame, cls).__new__(cls)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cmapper") 

        pixmap = QPixmap("app/assets/images/beautiful-shot-colorful-tulips-field-sunny-day.jpg").scaled(1024, 576)

        self.background_img = QLabel(self)
        self.background_img.setPixmap(pixmap)
        self.background_img.setGeometry(0, 0, OpenFrame.width, OpenFrame.height)

        self.setGeometry(0, 0, OpenFrame.width, OpenFrame.height)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("background-color: white;") 
        self.status_bar.showMessage("Loading...")

        QTimer.singleShot(3000, self.load_mainframe)

    def load_mainframe(self):
        try:
            self.main = MainFrame()
            self.main.show()
            self.close()
        except Exception as e:
            print("Error loading MainFrame:", e)
        

