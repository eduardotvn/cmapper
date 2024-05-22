from PyQt5 import QtCore, QtGui, QtWidgets
from utils.datasetInfo import turn_db_into_dataframe
from io import StringIO
from .buttons.buttonFuncs import run_encoder_dialog, run_drop_column_dialog, run_correlation_matrix_dialog
from .Dialogs.DataFrameHead import DataFrameDialog
from frames.buttons.mainFuncs import save_data


def load_corr_matrix_visualization(self, parent):
    self.running_feature.hide()
    
    self.CorrelationMatrixGB = QtWidgets.QGroupBox(parent)
    self.CorrelationMatrixGB.setGeometry(QtCore.QRect(210, 30, 811, 521))
    self.CorrelationMatrixGB.setTitle("")

    self.tablesOptions = QtWidgets.QComboBox(self.CorrelationMatrixGB)
    self.tablesOptions.setGeometry(QtCore.QRect(620, 5, 161, 32))
    self.tablesOptions.setObjectName("tablesOptions")
    self.tablesOptions.currentIndexChanged.connect(self.set_dataframe_table)

    self.CorrelationMatrixGB.setObjectName("CorrelationMatrixGB")
    self.textEdit = QtWidgets.QTextEdit(self.CorrelationMatrixGB)
    self.textEdit.setGeometry(QtCore.QRect(20, 40, 271, 461))
    self.textEdit.setObjectName("textEdit")
    self.textEdit.setReadOnly(True)

    self.DataOptions = QtWidgets.QGroupBox(self.CorrelationMatrixGB)
    self.DataOptions.setGeometry(QtCore.QRect(320, 40, 461, 461))
    self.DataOptions.setObjectName("DataOptions")

    self.DFInfoLabel = QtWidgets.QLabel(self.DataOptions)
    self.DFInfoLabel.setGeometry(QtCore.QRect(10, 10, 151, 31))
    self.DFInfoLabel.setText("Dataframe information:")

    self.DFInfoText = QtWidgets.QTextEdit(self.DataOptions)
    self.DFInfoText.setGeometry(QtCore.QRect(10, 40, 441, 191))

    self.DropColumnButton = QtWidgets.QPushButton(self.DataOptions)
    self.DropColumnButton.setGeometry(QtCore.QRect(30, 240, 88, 34))
    self.DropColumnButton.setText("Drop Column")
    self.DropColumnButton.clicked.connect(lambda: run_drop_column_dialog(self))

    self.EncodeColumnButton = QtWidgets.QPushButton(self.DataOptions)
    self.EncodeColumnButton.setGeometry(QtCore.QRect(130, 240, 88, 34))
    self.EncodeColumnButton.setText("Encode")
    self.EncodeColumnButton.clicked.connect(lambda: run_encoder_dialog(self))

    self.ReloadDFButton = QtWidgets.QPushButton(self.DataOptions)
    self.ReloadDFButton.setGeometry(QtCore.QRect(330, 240, 88, 34))
    self.ReloadDFButton.setText("Reload")
    self.ReloadDFButton.clicked.connect(lambda: reload_dataframe(self))

    self.DFHeadButton = QtWidgets.QPushButton(self.DataOptions)
    self.DFHeadButton.setGeometry(QtCore.QRect(230, 240,88, 34))
    self.DFHeadButton.setText("Preview")
    self.DFHeadButton.clicked.connect(lambda: show_dataframe_sample(self))

    self.GenerateCMButton = QtWidgets.QPushButton(self.DataOptions)
    self.GenerateCMButton.setGeometry(QtCore.QRect(375, 375, 81, 81))
    self.GenerateCMButton.setObjectName("Generate CM Button")
    self.GenerateCMButton.setText("Generate")
    self.GenerateCMButton.clicked.connect(lambda: run_correlation_matrix_dialog(self))

    self.saveDFButton = QtWidgets.QPushButton(self.DataOptions)
    self.saveDFButton.setGeometry(QtCore.QRect(275, 420, 88, 34))
    self.saveDFButton.setText("Save DF")
    self.saveDFButton.clicked.connect(lambda: save_data(self, self.current_dataframe))

    self.tablesOptions.addItems(self.found_tables)

    self.running_feature = self.CorrelationMatrixGB
    self.running_feature.show()


def reload_dataframe(self):
    self.refresh_df_info()

def show_dataframe_sample(self):
    df_sample = self.current_dataframe.head()
    self.dialog = DataFrameDialog(df_sample)
    self.dialog.exec_()
