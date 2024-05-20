from PyQt5 import QtCore, QtGui, QtWidgets
from .tabsButtons.PCA.loadPCAButtons import load_pca_buttons

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
    self.pcaDataframeInfo.setText(dataframe_info(self))
    self.pcaDataframeInfo.setStyleSheet("border: 1px solid black;")

    self.DimensionReductionTabs = QtWidgets.QTabWidget(self.PCAGB)
    self.DimensionReductionTabs.setGeometry(QtCore.QRect(5, 191, 800, 320))

    self.tab_pca = QtWidgets.QWidget()
    self.tab_lda = QtWidgets.QWidget()
    self.tab_tsne = QtWidgets.QWidget()
    self.DimensionReductionTabs.addTab(self.tab_pca, "PCA")
    self.DimensionReductionTabs.addTab(self.tab_lda, "LDA")
    self.DimensionReductionTabs.addTab(self.tab_tsne, "t-SNE")

    load_pca_buttons(self, self.tab_pca)

    self.running_feature = self.PCAGB
    self.running_feature.show()

def dataframe_info(self):
    cols = "Columns: " + f"{self.current_dataframe.columns.tolist()}" + "\n\n"
    na_counts_per_row = self.current_dataframe.isna().any(axis=1).sum()
    total_na_rows = self.current_dataframe.isna().sum().sum()
    info = f"This dataframe contains: {total_na_rows} missing values, in a total of {na_counts_per_row} rows"
    
    return cols + info 
