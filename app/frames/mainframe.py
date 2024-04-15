import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDialog
from PyQt5.QtGui import QPixmap

class MainFrame(QDialog):
    def __new__(cls):
        cls.height = 576
        cls.width = 1024
        return super(MainFrame, cls).__new__(cls)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cmapper")

        self.setGeometry(0, 0, MainFrame.width, MainFrame.height)