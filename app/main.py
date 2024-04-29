import sys
from frames import OpenFrame
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from db.connection.tableHandlers import check_tables
from dotenv import load_dotenv


if __name__ == "__main__":
    
    load_dotenv(".env")

    app = QApplication(sys.argv)
    window = OpenFrame()
    window.show()



    sys.exit(app.exec_())
