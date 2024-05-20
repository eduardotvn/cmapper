from PyQt5 import QtCore, QtGui, QtWidgets
from .buttons.mainButtons import refresh_db_visualization, run_creation_dialog, run_choose_container_dialog, run_db_insertion_dialog, run_delete_row_dialog, run_create_table_dialog, run_delete_db_dialog, run_update_row_dialog
from .buttons.mainFuncs import filter_db
from docker.findcontainers import run_container
from db.connection.tableHandlers import check_tables
from frames.mainframe_features.CorrelationMatrix.correlation_matrix_feature import load_corr_matrix_visualization
from frames.mainframe_features.PCA.pca_feature import load_pca_visualization
from utils.datasetInfo import turn_db_into_dataframe
from io import StringIO

class Ui_MainWindow(object):
    def __init__(self): 
        self.current_table = None 
        self.found_tables = []
        self.found_containers = []
        self.current_container = None 
        self.running_feature = None
        self.current_dataframe = None 

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 576)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.VisualizationGB = QtWidgets.QGroupBox(self.centralwidget)
        self.VisualizationGB.setGeometry(QtCore.QRect(210, 0, 811, 521))
        self.VisualizationGB.setObjectName("VisualizationGB")

        self.DBVisualization = QtWidgets.QTableWidget(self.VisualizationGB)
        self.DBVisualization.setGeometry(QtCore.QRect(30, 50, 741, 311))
        self.DBVisualization.setObjectName("DBVisualization")
        self.DBVisualization.setColumnCount(0)
        self.DBVisualization.setRowCount(0)

        self.FilterInput = QtWidgets.QLineEdit(self.VisualizationGB)
        self.FilterInput.setGeometry(QtCore.QRect(90, 390, 231, 41))
        self.FilterInput.setObjectName("FilterInput")
        self.FilterInput.returnPressed.connect(lambda: filter_db(self, self.current_table, self.FilterInput.text()))

        self.Columns = QtWidgets.QComboBox(self.VisualizationGB)
        self.Columns.setGeometry(QtCore.QRect(410, 390, 231, 41))
        self.Columns.setObjectName("Columns")

        self.Tables = QtWidgets.QComboBox(self.VisualizationGB)
        self.Tables.setGeometry(QtCore.QRect(540, 5, 231, 41))
        self.Tables.setObjectName("Tables")
        self.Tables.currentIndexChanged.connect(self.set_current_table)

        self.SearchLabel = QtWidgets.QLabel(self.VisualizationGB)
        self.SearchLabel.setGeometry(QtCore.QRect(340, 400, 71, 21))
        self.SearchLabel.setObjectName("SearchLabel")

        self.FilterLabel = QtWidgets.QLabel(self.VisualizationGB)
        self.FilterLabel.setGeometry(QtCore.QRect(50, 400, 31, 21))
        self.FilterLabel.setObjectName("FilterLabel")

        self.InputDataButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.InputDataButton.setGeometry(QtCore.QRect(30, 470, 88, 34))
        self.InputDataButton.setObjectName("InputDataButton")
        self.InputDataButton.clicked.connect(lambda: run_db_insertion_dialog(self))

        self.UpdateButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.UpdateButton.setGeometry(QtCore.QRect(150, 470, 88, 34))
        self.UpdateButton.setObjectName("UpdateButton")
        self.UpdateButton.clicked.connect(lambda: run_update_row_dialog(self))

        self.DeleteButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.DeleteButton.setGeometry(QtCore.QRect(270, 470, 88, 34))
        self.DeleteButton.setObjectName("DeleteButton")
        self.DeleteButton.clicked.connect(lambda: run_delete_row_dialog(self))
        
        self.DeleteDBButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.DeleteDBButton.setGeometry(QtCore.QRect(670, 470, 121, 34))
        self.DeleteDBButton.setObjectName("DeleteDBButton")
        self.DeleteDBButton.clicked.connect(lambda: run_delete_db_dialog(self))

        self.RefreshButton = QtWidgets.QPushButton(self.VisualizationGB)
        self.RefreshButton.setGeometry(QtCore.QRect(390, 470, 88, 34))
        self.RefreshButton.setObjectName("RefreshButton")
        self.RefreshButton.setText("Refresh")
        self.RefreshButton.clicked.connect(self.run_refresh)

        self.VisualizationButton = QtWidgets.QPushButton(self.centralwidget)
        self.VisualizationButton.setGeometry(QtCore.QRect(50, 20, 91, 91))
        self.VisualizationButton.setObjectName("VisualizationButton")
        self.VisualizationButton.clicked.connect(lambda: self.run_feature(self.running_feature, self.VisualizationGB))

        self.CorrelationButton = QtWidgets.QPushButton(self.centralwidget)
        self.CorrelationButton.setGeometry(QtCore.QRect(50, 120, 91, 91))
        self.CorrelationButton.setObjectName("CorrelationButton")
        self.CorrelationButton.clicked.connect(lambda: load_corr_matrix_visualization(self, MainWindow))

        self.ChartsButton = QtWidgets.QPushButton(self.centralwidget)
        self.ChartsButton.setGeometry(QtCore.QRect(50, 320, 91, 91))
        self.ChartsButton.setObjectName("ChartsButton")
        self.ChartsButton.clicked.connect(self.VisualizationGB.hide)

        self.PCAButton = QtWidgets.QPushButton(self.centralwidget)
        self.PCAButton.setGeometry(QtCore.QRect(50, 220, 91, 91))
        self.PCAButton.setObjectName("PCAButton")
        self.PCAButton.clicked.connect(lambda: load_pca_visualization(self, MainWindow))

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

        self.menuDocker = QtWidgets.QMenu(self.menubar)
        self.menuDocker.setObjectName("menuDocker")

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
        self.actionOpen.triggered.connect(lambda: run_creation_dialog(self))

        self.actionSelect_DB = QtWidgets.QAction(MainWindow)
        self.actionSelect_DB.setObjectName("actionSelect_DB")

        self.actionCreate_DB = QtWidgets.QAction(MainWindow)
        self.actionCreate_DB.setObjectName("actionCreate_DB")
        self.actionCreate_DB.triggered.connect(lambda: run_create_table_dialog(self))

        self.actionSelect_Docker = QtWidgets.QAction(MainWindow)
        self.actionSelect_Docker.setObjectName("actionSelect_Docker")  
        self.actionSelect_Docker.triggered.connect(lambda: run_choose_container_dialog(self))

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
        self.menuDatabase.addAction(self.actionCreate_DB)

        self.menuDocker.addAction(self.actionSelect_Docker)

        self.menuHelp.addAction(self.actionAbout_Cmapper)
        self.menuHelp.addAction(self.actionManual)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())
        self.menubar.addAction(self.menuDocker.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.running_feature = self.VisualizationGB

    def set_container_data(self, containers : list):
        if len(containers) == 0:
            return 
        self.current_container = containers[0].split()[-1]
        self.found_containers = [name.split()[-1] for name in containers] 
        self.run_chosen_container()
        self.set_tables()

    def set_tables(self):
        try: 
            tables = check_tables()
            if len(tables) == 0:
                return 
            self.Tables.currentIndexChanged.disconnect(self.set_current_table)
            self.found_tables = [table[0] for table in tables]
            self.current_table = self.found_tables[0] 
            self.Tables.clear()
            self.Tables.addItems(self.found_tables)
            self.run_refresh()
            self.Tables.currentIndexChanged.connect(self.set_current_table)
        except Exception as e: 
            print("Something went wrong while trying to set tables: ", e)
            self.Tables.currentIndexChanged.connect(self.set_current_table)
    
    def set_current_table(self):
        table = self.Tables.currentText()
        self.current_table = table
        self.run_refresh()

    def run_chosen_container(self):
        if run_container(self.current_container):
            print("Succesfully running container")
        else: 
            print("Something went wrong")

    def run_refresh(self):
        tables = [table[0] for table in check_tables()] 
        if self.current_table in tables:
            refresh_db_visualization(self, self.current_table)
        else: 
            self.set_tables()

    def run_feature(self, running_feature, feature):
        if running_feature is not None:
            running_feature.hide()
            feature.show()
        else:
            return 
    def set_dataframe_table(self):
        self.current_table = self.tablesOptions.currentText()
        self.refresh_df_info()

    def set_dataframe(self):
        self.current_dataframe = turn_db_into_dataframe(self.current_table)

    def refresh_df_info(self):
        self.textEdit.setReadOnly(False)

        df = turn_db_into_dataframe(self.current_table)
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        info_str = info_str.replace("<class 'pandas.core.frame.DataFrame'>\n", "")
        self.textEdit.setText(info_str)

        self.textEdit.setReadOnly(True)
        self.current_dataframe = df
        self.set_current_dataframe_info()

    def set_current_dataframe_info(self):
        if self.current_dataframe is not None: 
            cols = self.current_dataframe.columns.tolist()
            self.DFInfoText.setText(f"Current columns: {cols}, TOTAL: {len(cols)}")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cmapper"))
        self.VisualizationGB.setTitle(_translate("MainWindow", "Database Visualization"))
        self.SearchLabel.setText(_translate("MainWindow", "Search in"))
        self.FilterLabel.setText(_translate("MainWindow", "Filter"))
        self.InputDataButton.setText(_translate("MainWindow", "Input"))
        self.UpdateButton.setText(_translate("MainWindow", "Update"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete"))
        self.DeleteDBButton.setText(_translate("MainWindow", "Delete Database"))
        self.RefreshButton.setText(_translate("MainWindow", "Refresh"))
        self.VisualizationButton.setText(_translate("MainWindow", "Visualization"))
        self.ChartsButton.setText(_translate("MainWindow", "Charts"))
        self.PCAButton.setText(_translate("MainWindow", "PCA"))
        self.CorrelationButton.setText(_translate("MainWindow", "Correlation"))
        self.OtherButton.setText(_translate("MainWindow", "Other"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDatabase.setTitle(_translate("MainWindow", "Database"))
        self.menuDocker.setTitle(_translate("MainWindow", "Docker"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionClose.setText(_translate("MainWindow", "Close "))
        self.actionOpen.setText(_translate("MainWindow", "Choose File"))
        self.actionSelect_DB.setText(_translate("MainWindow", "Select DB"))
        self.actionCreate_DB.setText(_translate("MainWindow", "Create Database"))
        self.actionSelect_Docker.setText(_translate("MainWindow", "Select Docker"))
        self.actionLoad_CSV.setText(_translate("MainWindow", "Load File "))
        self.actionRecent.setText(_translate("MainWindow", "Recent "))
        self.actionAbout_Cmapper.setText(_translate("MainWindow", "About Cmapper"))
        self.actionManual.setText(_translate("MainWindow", "Manual"))
