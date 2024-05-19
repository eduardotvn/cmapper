from PyQt5 import QtCore, QtGui, QtWidgets
from utils.datasetInfo import turn_db_into_dataframe
from io import StringIO
from .buttons.buttonFuncs import run_encoder_dialog

def load_corr_matrix_visualization(self, parent):
    self.running_feature.hide()
    
    self.CorrelationMatrixGB = QtWidgets.QGroupBox(parent)
    self.CorrelationMatrixGB.setGeometry(QtCore.QRect(210, 30, 811, 521))
    self.CorrelationMatrixGB.setTitle("")

    self.tablesOptions = QtWidgets.QComboBox(self.CorrelationMatrixGB)
    self.tablesOptions.setGeometry(QtCore.QRect(620, 5, 161, 32))
    self.tablesOptions.setObjectName("tablesOptions")
    self.tablesOptions.currentIndexChanged.connect(lambda: set_dataframe_table(self))

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
    self.DropColumnButton.setGeometry(QtCore.QRect(10, 240, 88, 34))
    self.DropColumnButton.setText("Drop Column")

    self.EncodeColumnButton = QtWidgets.QPushButton(self.DataOptions)
    self.EncodeColumnButton.setGeometry(QtCore.QRect(110, 240, 88, 34))
    self.EncodeColumnButton.setText("Encode")
    self.EncodeColumnButton.clicked.connect(lambda: run_encoder_dialog(self))

    self.ReloadDFButton = QtWidgets.QPushButton(self.DataOptions)
    self.ReloadDFButton.setGeometry(QtCore.QRect(360, 240, 88, 34))
    self.ReloadDFButton.setText("Reload")

    self.GenerateCMButton = QtWidgets.QPushButton(self.DataOptions)
    self.GenerateCMButton.setGeometry(QtCore.QRect(375, 375, 81, 81))
    self.GenerateCMButton.setObjectName("Generate CM Button")
    self.GenerateCMButton.setText("Generate")

    self.tablesOptions.addItems(self.found_tables)

    self.running_feature = self.CorrelationMatrixGB
    self.running_feature.show()

def set_dataframe_table(self):
    self.current_table = self.tablesOptions.currentText()
    refresh_df_info(self)

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
    set_current_dataframe_info(self)

def set_current_dataframe_info(self):
    if self.current_dataframe is not None: 
        cols = self.current_dataframe.columns.tolist()
        self.DFInfoText.setText(f"Current columns: {cols}, TOTAL: {len(cols)}")
