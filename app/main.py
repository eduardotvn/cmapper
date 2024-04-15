import sys
from frames import OpenFrame
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenFrame()
    window.show()
    sys.exit(app.exec_())
