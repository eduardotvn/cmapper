from PyQt5 import QtCore, QtGui, QtWidgets
from .buttons.mainButtons import refresh_db_visualization, run_creation_dialog, run_create_container_dialog, run_db_insertion_dialog, run_delete_row_dialog, run_create_table_dialog, run_delete_db_dialog, run_update_row_dialog, run_about_dialog
from .buttons.mainFuncs import filter_db
from docker.findcontainers import run_container
from PyQt5.QtWidgets import QTableWidgetItem
from db.connection.tableHandlers import check_tables
from frames.mainframe_features.DataframeEdit.dataframeEditFeature import load_dataframe_edit_feature
from frames.mainframe_features.DimensionalReduction.pca_feature import load_pca_visualization
from frames.mainframe_features.MachineLearning.MLTabs import load_machine_learning_tabs
from frames.mainframe_features.Plot.load_plotting_feature import load_plotting_features
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
        self.clusterized_dataframe = None  
        self.current_dataframe_type = None
        self.clusterized_dataframe_type = None 

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 576)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.VisualizationGB = QtWidgets.QGroupBox(self.centralwidget)
        self.VisualizationGB.setGeometry(QtCore.QRect(210, 0, 811, 531))
        self.VisualizationGB.setObjectName("VisualizationGB")

        self.DBVisualization = QtWidgets.QTableWidget(self.VisualizationGB)
        self.DBVisualization.setGeometry(QtCore.QRect(30, 50, 741, 311))
        self.DBVisualization.setObjectName("DBVisualization")
        self.DBVisualization.setColumnCount(0)
        self.DBVisualization.setRowCount(0)
        self.DBVisualization.setStyleSheet("border: 1px solid black;")

        self.FilterInput = QtWidgets.QLineEdit(self.VisualizationGB)
        self.FilterInput.setGeometry(QtCore.QRect(90, 390, 231, 41))
        self.FilterInput.setObjectName("FilterInput")
        self.FilterInput.returnPressed.connect(lambda: filter_db(self, self.current_table, self.FilterInput.text()))

        self.Columns = QtWidgets.QComboBox(self.VisualizationGB)
        self.Columns.setGeometry(QtCore.QRect(410, 390, 231, 41))
        self.Columns.setObjectName("Columns")

        self.Tables = QtWidgets.QComboBox(self.VisualizationGB)
        self.Tables.setGeometry(QtCore.QRect(500, 5, 231, 41))
        self.Tables.setObjectName("Tables")
        self.Tables.currentIndexChanged.connect(self.set_current_table)

        self.AdvancedOptions = QtWidgets.QToolButton(self.VisualizationGB)
        self.AdvancedOptions.setGeometry(QtCore.QRect(735, 5, 40, 40))
        self.AdvancedOptions.setText("...")

        self.AdvancedOptionsMenu = QtWidgets.QMenu(self.AdvancedOptions)

        self.AddColumn_Action = QtWidgets.QAction(self.AdvancedOptions)
        self.AddColumn_Action.setText("Add Column")

        self.SumTables_Action = QtWidgets.QAction(self.AdvancedOptions)
        self.SumTables_Action.setText("Sum Tables")

        self.DeleteColumn_Action = QtWidgets.QAction(self.AdvancedOptions)
        self.DeleteColumn_Action.setText("Delete Column")

        self.AdvancedOptionsMenu.addAction(self.AddColumn_Action)
        self.AdvancedOptionsMenu.addAction(self.SumTables_Action)
        self.AdvancedOptionsMenu.addAction(self.DeleteColumn_Action)
        self.AdvancedOptions.setMenu(self.AdvancedOptionsMenu)

        self.AdvancedOptions.setPopupMode(QtWidgets.QToolButton.InstantPopup)

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
        self.CorrelationButton.clicked.connect(lambda: load_dataframe_edit_feature(self, MainWindow))

        self.PlottingButton = QtWidgets.QPushButton(self.centralwidget)
        self.PlottingButton.setGeometry(QtCore.QRect(50, 320, 91, 91))
        self.PlottingButton.setObjectName("PlottingButton")
        self.PlottingButton.clicked.connect(lambda: load_plotting_features(self, MainWindow))

        self.DRButton = QtWidgets.QPushButton(self.centralwidget)
        self.DRButton.setGeometry(QtCore.QRect(50, 220, 91, 91))
        self.DRButton.setObjectName("DRButton")
        self.DRButton.clicked.connect(lambda: load_pca_visualization(self, MainWindow))

        self.MLButton = QtWidgets.QPushButton(self.centralwidget)
        self.MLButton.setGeometry(QtCore.QRect(50, 420, 91, 91))
        self.MLButton.setObjectName("MLButton")
        self.MLButton.clicked.connect(lambda: load_machine_learning_tabs(self, MainWindow))

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
        self.actionClose.triggered.connect(MainWindow.close)

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(lambda: run_creation_dialog(self))

        self.actionSelect_DB = QtWidgets.QAction(MainWindow)
        self.actionSelect_DB.setObjectName("actionSelect_DB")

        self.actionCreate_DB = QtWidgets.QAction(MainWindow)
        self.actionCreate_DB.setObjectName("actionCreate_DB")
        self.actionCreate_DB.triggered.connect(lambda: run_create_table_dialog(self))

        self.actionCreate_Container = QtWidgets.QAction(MainWindow)
        self.actionCreate_Container.setObjectName("actionCreate_Container")  
        self.actionCreate_Container.triggered.connect(lambda: run_create_container_dialog(self))

        self.actionLoad_CSV = QtWidgets.QAction(MainWindow)
        self.actionLoad_CSV.setObjectName("actionLoad_CSV")

        self.actionAbout_Cmapper = QtWidgets.QAction(MainWindow)
        self.actionAbout_Cmapper.setObjectName("actionAbout_Cmapper")
        self.actionAbout_Cmapper.triggered.connect(lambda: run_about_dialog(self))

        self.actionManual = QtWidgets.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)

        self.menuDatabase.addAction(self.actionSelect_DB)
        self.menuDatabase.addAction(self.actionCreate_DB)

        self.menuDocker.addAction(self.actionCreate_Container)

        self.menuHelp.addAction(self.actionAbout_Cmapper)
        self.menuHelp.addAction(self.actionManual)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())
        self.menubar.addAction(self.menuDocker.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.running_feature = self.VisualizationGB
        self.window = MainWindow

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
                self.Tables.clear()
                self.DBVisualization.clear()
                self.DBVisualization.setRowCount(0)
                self.DBVisualization.setColumnCount(0)
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
        self.current_dataframe_type = None
        self.set_current_dataframe_info()

    def set_current_dataframe_info(self):
        if self.current_dataframe is not None: 
            cols = self.current_dataframe.columns.tolist()
            self.DFInfoText.setText(f"Current columns: {cols}, TOTAL: {len(cols)}")

    def populate_pca_table(self):
        if self.current_dataframe_type == "PCA":
            target = self.PCAInfoData
        elif self.current_dataframe_type == "LDA":
            target = self.LDAInfoData
        elif self.current_dataframe_type == "TSNE":
            target = self.TSNEInfoData

        df = self.current_dataframe.copy()
        target.clearContents()
        target.setRowCount(df.shape[0]) 
        target.setColumnCount(df.shape[1])  
        target.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):  
            for j in range(df.shape[1]): 
                item = QTableWidgetItem(str(df.iloc[i, j]))  
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable) 
                target.setItem(i, j, item)

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
        self.VisualizationButton.setText(_translate("MainWindow", "Database\nVisualization"))
        self.PlottingButton.setText(_translate("MainWindow", "Plotting"))
        self.DRButton.setText(_translate("MainWindow", "Dimensional\nReduction"))
        self.CorrelationButton.setText(_translate("MainWindow", "Edit\nDataframe"))
        self.MLButton.setText(_translate("MainWindow", "Machine\nLearning"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDatabase.setTitle(_translate("MainWindow", "Database"))
        self.menuDocker.setTitle(_translate("MainWindow", "Docker"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionClose.setText(_translate("MainWindow", "Close "))
        self.actionOpen.setText(_translate("MainWindow", "Choose File"))
        self.actionSelect_DB.setText(_translate("MainWindow", "Select DB"))
        self.actionCreate_DB.setText(_translate("MainWindow", "Create Database"))
        self.actionCreate_Container.setText(_translate("MainWindow", "Create Container"))
        self.actionLoad_CSV.setText(_translate("MainWindow", "Load File "))
        self.actionAbout_Cmapper.setText(_translate("MainWindow", "About Cmapper"))
        self.actionManual.setText(_translate("MainWindow", "Manual"))
