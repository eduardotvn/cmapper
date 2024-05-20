from PyQt5 import QtCore, QtGui, QtWidgets

def load_pca_visualization(self, parent):
    self.running_feature.hide()
    if self.current_dataframe is None:
        self.set_dataframe()

    self.PCAGB = QtWidgets.QGroupBox(parent)
    self.PCAGB.setGeometry(QtCore.QRect(210, 30, 811, 521))
    self.PCAGB.setTitle("")

    self.NoteLabel = QtWidgets.QLabel(self.PCAGB)
    self.NoteLabel.setGeometry(QtCore.QRect(10, 10, 461, 31))
    self.NoteLabel.setText("Note: This feature will use the dataframe produced by Correlation feature.\nIf you need to edit it, click on Correlation and apply transformations.")

    self.pcaDataframeInfo = QtWidgets.QTextEdit(self.PCAGB)
    self.pcaDataframeInfo.setGeometry(QtCore.QRect(5, 50, 801, 121))
    self.pcaDataframeInfo.setText(self.current_dataframe.describe().to_string())

    self.running_feature = self.PCAGB
    self.running_feature.show()
