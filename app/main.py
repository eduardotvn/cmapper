import sys
from frames import OpenFrame
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from db.connection.tableHandlers import check_tables
from db.fileHandling.csvIntoPostgres import try_table_creation, try_table_insertion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenFrame()
    window.show()

    if try_table_creation("sample_database_2", "app/db/sampleCSV/Mall_Customers.csv"):
        print("Sample database 2 created")
    if try_table_insertion("sample_database_2", "app/db/sampleCSV/Mall_Customers.csv"):
        print("Sample Database created")
    sys.exit(app.exec_())
