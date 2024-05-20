from PyQt5 import QtCore, QtGui, QtWidgets
from frames.mainframe_features.CorrelationMatrix.Dialogs.EncoderDialog import Ui_EncoderDialog
from frames.mainframe_features.CorrelationMatrix.Dialogs.DropColumnDialog import Ui_DropColDialog
from frames.mainframe_features.CorrelationMatrix.Dialogs.CorrelationMatrix import CorrelationMatrixDialog

def run_encoder_dialog(self):

    self.Encoder_Dialog = QtWidgets.QDialog()
    self.EDialog = Ui_EncoderDialog()
    self.EDialog.setupUi(self.Encoder_Dialog)
    self.EDialog.df = self.current_dataframe
    self.EDialog.set_options(self.current_dataframe.columns.tolist())
    self.EDialog.parent = self
    self.Encoder_Dialog.show()

def run_drop_column_dialog(self):

    self.DropColumn_Dialog = QtWidgets.QDialog()
    self.DCDialog = Ui_DropColDialog()
    self.DCDialog.setupUi(self.DropColumn_Dialog)
    self.DCDialog.current_dataframe = self.current_dataframe
    self.DCDialog.set_cols_options(self.current_dataframe.columns.tolist())
    self.DCDialog.parent = self
    self.DropColumn_Dialog.show()

def run_correlation_matrix_dialog(self):
    if self.current_dataframe is not None:
        df = self.current_dataframe.dropna()
        df_corr = df.corr()
        self.dialog = CorrelationMatrixDialog(df_corr)
        self.dialog.exec_()