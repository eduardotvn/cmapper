from PyQt5 import QtCore, QtGui, QtWidgets
from utils.encodeColumn import encode_column

class Ui_EncoderDialog(object):
    def __init__(self):
        self.df = None
    def setupUi(self, EncoderDialog):
        EncoderDialog.setObjectName("EncoderDialog")
        EncoderDialog.resize(450, 111)

        self.ColumnLabel = QtWidgets.QLabel(EncoderDialog)
        self.ColumnLabel.setGeometry(QtCore.QRect(10, 20, 61, 31))
        self.ColumnLabel.setObjectName("ColumnLabel")

        self.ColumnOptions = QtWidgets.QComboBox(EncoderDialog)
        self.ColumnOptions.setGeometry(QtCore.QRect(70, 20, 141, 32))
        self.ColumnOptions.setObjectName("ColumnOptions")

        self.EncoderLabel = QtWidgets.QLabel(EncoderDialog)
        self.EncoderLabel.setGeometry(QtCore.QRect(220, 17, 61, 31))
        self.EncoderLabel.setObjectName("EncoderLabel")

        self.EncoderOptions = QtWidgets.QComboBox(EncoderDialog)
        self.EncoderOptions.setGeometry(QtCore.QRect(290, 20, 151, 32))
        self.EncoderOptions.setObjectName("EncoderOptions")

        self.EncodeButton = QtWidgets.QPushButton(EncoderDialog)
        self.EncodeButton.setGeometry(QtCore.QRect(10, 70, 88, 34))
        self.EncodeButton.setObjectName("EncodeButton")
        self.EncodeButton.clicked.connect(lambda: self.encode_column(EncoderDialog))

        self.CancelButton = QtWidgets.QPushButton(EncoderDialog)
        self.CancelButton.setGeometry(QtCore.QRect(350, 70, 88, 34))
        self.CancelButton.setObjectName("CancelButton")
        self.CancelButton.clicked.connect(EncoderDialog.close)

        self.retranslateUi(EncoderDialog)
        QtCore.QMetaObject.connectSlotsByName(EncoderDialog)

    def encode_column(self, EncoderDialog):
        col = self.ColumnOptions.currentText()
        encoder = self.EncoderOptions.currentText()
        encode_column(self.df, col, encoder)

    def set_options(self, cols):
        self.EncoderOptions.addItems(encoder_options)
        self.ColumnOptions.addItems(cols)
        
    def retranslateUi(self, EncoderDialog):
        _translate = QtCore.QCoreApplication.translate
        EncoderDialog.setWindowTitle(_translate("EncoderDialog", "Choose Column to Encode"))
        self.ColumnLabel.setText(_translate("EncoderDialog", "Column:"))
        self.EncoderLabel.setText(_translate("EncoderDialog", "Encoder:"))
        self.EncodeButton.setText(_translate("EncoderDialog", "Encode"))
        self.CancelButton.setText(_translate("EncoderDialog", "Cancel"))

encoder_options = ["One-Hot Encoder", "Label Encoder", "Ordinal Encoder"]
