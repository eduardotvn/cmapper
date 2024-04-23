import sys
from frames import OpenFrame
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from db.connection.tableHandlers import check_tables
from dotenv import load_dotenv


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = OpenFrame()
    window.show()

    load_dotenv(".env")

    sys.exit(app.exec_())
