import sys
from frames import OpenFrame
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from db.connection.tableHandlers import check_tables
from db.fileHandling.csvIntoPostgres import try_table_creation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenFrame()
    window.show()

    if try_table_creation("sample_database", "app/db/sampleCSV/marketing_campaign.csv"):
        print("Success")

    sys.exit(app.exec_())
