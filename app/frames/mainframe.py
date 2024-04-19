from PyQt5 import QtCore, QtGui, QtWidgets
from .buttons.mainButtons import refresh_db_visualization
from .dialogs.createDbDialog import Ui_CreateDatabaseFromFile
from .buttons.mainFuncs import filter_db

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 576)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.VisualizationGB = QtWidgets.QGroupBox(self.centralwidget)
        self.VisualizationGB.setGeometry(QtCore.QRect(210, 0, 811, 521))
        self.VisualizationGB.setObjectName("VisualizationGB")

        self.DBVisualization = QtWidgets.QTableWidget(self.VisualizationGB)
        self.DBVisualization.setGeometry(QtCore.QRect(30, 30, 741, 351))
        self.DBVisualization.setObjectName("DBVisualization")
        self.DBVisualization.setColumnCount(0)
        self.DBVisualization.setRowCount(0)

        self.FilterInput = QtWidgets.QLineEdit(self.VisualizationGB)
        self.FilterInput.setGeometry(QtCore.QRect(90, 390, 231, 41))
        self.FilterInput.setObjectName("FilterInput")
        self.FilterInput.returnPressed.connect(lambda: filter_db(self, "sample_database", self.FilterInput.text()))

        self.Columns = QtWidgets.QComboBox(self.VisualizationGB)
        self.Columns.setGeometry(QtCore.QRect(410, 390, 231, 41))
        self.Columns.setObjectName("Columns")

        self.SearchLabel = QtWidgets.QLabel(self.VisualizationGB)
        self.SearchLabel.setGeometry(QtCore.QRect(340, 400, 71, 21))
        self.SearchLabel.setObjectName("SearchLabel")

        self.FilterLabel = QtWidgets.QLabel(self.VisualizationGB)
        self.FilterLabel.setGeometry(QtCore.QRect(50, 400, 31, 21))
        self.FilterLabel.setObjectName("FilterLabel")

        self.InputDataButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.InputDataButton.setGeometry(QtCore.QRect(30, 470, 88, 34))
        self.InputDataButton.setObjectName("InputDataButton")

        self.UpdateButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.UpdateButton.setGeometry(QtCore.QRect(150, 470, 88, 34))
        self.UpdateButton.setObjectName("UpdateButton")

        self.DeleteButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.DeleteButton.setGeometry(QtCore.QRect(270, 470, 88, 34))
        self.DeleteButton.setObjectName("DeleteButton")
        
        self.AlterDBButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.AlterDBButton.setGeometry(QtCore.QRect(670, 470, 121, 34))
        self.AlterDBButton.setObjectName("AlterDBButton")

        self.RefreshButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.RefreshButton.setGeometry(QtCore.QRect(390, 470, 88, 34))
        self.RefreshButton.setObjectName("RefreshButton")
        self.RefreshButton.setText("Refresh")
        self.RefreshButton.clicked.connect(lambda: refresh_db_visualization(self, "sample_database"))

        self.VisualizationButton = QtWidgets.QPushButton(self.centralwidget)
        self.VisualizationButton.setGeometry(QtCore.QRect(50, 20, 91, 91))
        self.VisualizationButton.setObjectName("VisualizationButton")

        self.ChartsButton = QtWidgets.QPushButton(self.centralwidget)
        self.ChartsButton.setGeometry(QtCore.QRect(50, 120, 91, 91))
        self.ChartsButton.setObjectName("ChartsButton")

        self.PCAButton = QtWidgets.QPushButton(self.centralwidget)
        self.PCAButton.setGeometry(QtCore.QRect(50, 220, 91, 91))
        self.PCAButton.setObjectName("PCAButton")

        self.CorrelationButton = QtWidgets.QPushButton(self.centralwidget)
        self.CorrelationButton.setGeometry(QtCore.QRect(50, 320, 91, 91))
        self.CorrelationButton.setObjectName("CorrelationButton")

        self.OtherButton = QtWidgets.QPushButton(self.centralwidget)
        self.OtherButton.setGeometry(QtCore.QRect(50, 420, 91, 91))
        self.OtherButton.setObjectName("OtherButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1029, 30))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuDatabase = QtWidgets.QMenu(self.menubar)
        self.menuDatabase.setObjectName("menuDatabase")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.run_creation_dialog)

        self.actionSelect_DB = QtWidgets.QAction(MainWindow)
        self.actionSelect_DB.setObjectName("actionSelect_DB")

        self.actionLoad_CSV = QtWidgets.QAction(MainWindow)
        self.actionLoad_CSV.setObjectName("actionLoad_CSV")

        self.actionRecent = QtWidgets.QAction(MainWindow)
        self.actionRecent.setObjectName("actionRecent")

        self.actionAbout_Cmapper = QtWidgets.QAction(MainWindow)
        self.actionAbout_Cmapper.setObjectName("actionAbout_Cmapper")

        self.actionManual = QtWidgets.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionRecent)
        self.menuFile.addAction(self.actionClose)

        self.menuDatabase.addAction(self.actionSelect_DB)

        self.menuHelp.addAction(self.actionAbout_Cmapper)
        self.menuHelp.addAction(self.actionManual)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def run_creation_dialog(self):
        self.Creatrion_Dialog = QtWidgets.QDialog()
        self.CDialog = Ui_CreateDatabaseFromFile()
        self.CDialog.setupUi(self.Creatrion_Dialog)
        self.Creatrion_Dialog.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cmapper"))
        self.VisualizationGB.setTitle(_translate("MainWindow", "Database Visualization"))
        self.SearchLabel.setText(_translate("MainWindow", "Search in"))
        self.FilterLabel.setText(_translate("MainWindow", "Filter"))
        self.InputDataButton.setText(_translate("MainWindow", "Input"))
        self.UpdateButton.setText(_translate("MainWindow", "Update"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete"))
        self.AlterDBButton.setText(_translate("MainWindow", "Alter Database"))
        self.RefreshButton.setText(_translate("MainWindow", "Refresh"))
        self.VisualizationButton.setText(_translate("MainWindow", "Visualization"))
        self.ChartsButton.setText(_translate("MainWindow", "Charts"))
        self.PCAButton.setText(_translate("MainWindow", "PCA"))
        self.CorrelationButton.setText(_translate("MainWindow", "Correlation"))
        self.OtherButton.setText(_translate("MainWindow", "Other"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDatabase.setTitle(_translate("MainWindow", "Database"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionClose.setText(_translate("MainWindow", "Close "))
        self.actionOpen.setText(_translate("MainWindow", "Choose File"))
        self.actionSelect_DB.setText(_translate("MainWindow", "Select DB"))
        self.actionLoad_CSV.setText(_translate("MainWindow", "Load File "))
        self.actionRecent.setText(_translate("MainWindow", "Recent "))
        self.actionAbout_Cmapper.setText(_translate("MainWindow", "About Cmapper"))
        self.actionManual.setText(_translate("MainWindow", "Manual"))
