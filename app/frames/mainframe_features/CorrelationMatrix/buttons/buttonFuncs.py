from PyQt5 import QtCore, QtGui, QtWidgets
from frames.mainframe_features.CorrelationMatrix.Dialogs.EncoderDialog import Ui_EncoderDialog

def run_encoder_dialog(self):

    self.Encoder_Dialog = QtWidgets.QDialog()
    self.EDialog = Ui_EncoderDialog()
    self.EDialog.setupUi(self.Encoder_Dialog)
    self.EDialog.df = self.current_dataframe
    self.EDialog.set_options(self.current_dataframe.columns.tolist())
    self.Encoder_Dialog.show()