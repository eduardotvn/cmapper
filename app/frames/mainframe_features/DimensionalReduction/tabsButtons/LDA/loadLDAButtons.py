from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from utils.applyLDA import apply_lda
from frames.buttons.mainFuncs import run_save_processed_df
from frames.widgets.DfPlot import PlotWidget

def load_LDA_buttons(self, parent):
    
    self.numComponentsLabel = QtWidgets.QLabel(parent)
    self.numComponentsLabel.setGeometry(QtCore.QRect(5, 30, 150, 30))
    self.numComponentsLabel.setText("Number of components:")

    self.numComponentsInputLDA = QtWidgets.QLineEdit(parent)
    self.numComponentsInputLDA.setGeometry(QtCore.QRect(160, 30, 150, 30))
    
    self.scalerLabel = QtWidgets.QLabel(parent)
    self.scalerLabel.setGeometry(QtCore.QRect(5, 65, 100, 30))
    self.scalerLabel.setText("Scaler:")

    self.scalerOptions = QtWidgets.QComboBox(parent)
    self.scalerOptions.setGeometry(QtCore.QRect(160, 65, 150, 30))
    self.scalerOptions.addItems(["Standard", "MinMax", "MaxAbs"])

    self.targetLabel = QtWidgets.QLabel(parent)
    self.targetLabel.setGeometry(QtCore.QRect(5, 100, 100, 30))
    self.targetLabel.setText("Target Col:") 

    self.targetColCB = QtWidgets.QComboBox(parent)
    self.targetColCB.setGeometry(QtCore.QRect(160, 100, 150, 30))
    self.targetColCB.addItems(self.current_dataframe.columns.tolist())

    self.ignoreColLabel = QtWidgets.QLabel(parent)
    self.ignoreColLabel.setGeometry(QtCore.QRect(5,140, 100, 30))
    self.ignoreColLabel.setText("Ignore Column")

    self.ignoreColOptions = QtWidgets.QComboBox(parent)
    self.ignoreColOptions.setGeometry(QtCore.QRect(160, 140, 150, 30))
    self.ignoreColOptions.addItems(["None"] + self.current_dataframe.columns.tolist())

    self.generateLDAButton = QtWidgets.QPushButton(parent)
    self.generateLDAButton.setGeometry(QtCore.QRect(222,180, 88,34))
    self.generateLDAButton.setText("Generate")
    self.generateLDAButton.clicked.connect(lambda: generate_LDA_information(self))

    self.LDAInfoData = QtWidgets.QTableWidget(parent)
    self.LDAInfoData.setGeometry(QtCore.QRect(350, 30, 400, 200))
    self.LDAInfoData.setStyleSheet("border: 1px solid black;")

    self.plotButton = QtWidgets.QPushButton(parent)
    self.plotButton.setGeometry(QtCore.QRect(665, 240, 88, 34))
    self.plotButton.setText("Plot")
    self.plotButton.clicked.connect(lambda: run_plot_widget(self))

    self.saveDFButton = QtWidgets.QPushButton(parent)
    self.saveDFButton.setGeometry(QtCore.QRect(565, 240, 88, 34))
    self.saveDFButton.setText("Save DF")
    self.saveDFButton.clicked.connect(lambda: run_save_processed_df(self))

    self.accLabel = QtWidgets.QLabel(parent)
    self.accLabel.setGeometry(QtCore.QRect(350, 230, 250, 30))
    
    if self.current_dataframe_type is not None: 
        self.populate_pca_table()

def run_plot_widget(self):
    if self.current_dataframe is None:
        QMessageBox.critical(self.window, "Error", "No processed dataframe to be plotted")
        return 
    if 'Predictions' in self.current_dataframe.columns:
        if len(self.current_dataframe.columns.tolist()) == 3:
            labels = self.current_dataframe['Predictions']
            data = self.current_dataframe.drop(columns=['Predictions'])
            plot_widget = PlotWidget(data, labels=labels)
        elif len(self.current_dataframe.columns.tolist()) == 4: 
            labels = self.current_dataframe['Predictions']
            data = self.current_dataframe.drop(columns=['Predictions'])
            plot_widget = PlotWidget(data, labels=labels, plot_type='3D')
        else:
            QMessageBox.warning(self.window, "Error", f"Not possible to plot with {len(self.current_dataframe.columns.tolist()) - 1} features")
            return 
    else:
        if len(self.current_dataframe.columns.tolist()) == 2:
            plot_widget = PlotWidget(self.current_dataframe)
        elif len(self.current_dataframe.columns.tolist()) == 3:
            plot_widget = PlotWidget(self.current_dataframe, plot_type='3D')
        else:
            QMessageBox.warning(self.window, "Error", f"Not possible to plot with {len(self.current_dataframe.columns.tolist()) - 1} features")
            return 
    plot_widget.exec_()


def generate_LDA_information(self):
    target = self.targetColCB.currentText()
    dataframe = self.current_dataframe.copy()
    n_comps = self.numComponentsInputLDA.text()
    scaler = self.scalerOptions.currentText()
    ignoreCol = self.ignoreColOptions.currentText()

    if not n_comps.isdigit() or n_comps == '' or int(n_comps) > len(self.current_dataframe.columns.tolist()) or int(n_comps) <= 0:
        QMessageBox.warning(self.window, "Invalid value", "Insert a valid number of components")
        return 

    n_comps = int(n_comps)

    if ignoreCol != "None":
        results, acc, err = apply_lda(dataframe.drop(ignoreCol), n_comps, scaler, target)
    else: 
        results, acc, err = apply_lda(dataframe, n_comps, scaler, target)
        
    if err is not None:
        QMessageBox.critical(self.window, "Error", f"{str(err)}")
    else: 
        dataframe['Predictions'] = results
        dataframe = dataframe.drop(columns=[target])
        self.current_dataframe = dataframe
        self.current_dataframe_type = "LDA"
        self.accLabel.setText(f"Accuracy: {acc:.4f}")
        self.populate_pca_table()
