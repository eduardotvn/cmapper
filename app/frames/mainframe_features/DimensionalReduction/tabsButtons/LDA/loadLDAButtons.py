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

    self.generateLDAButton = QtWidgets.QPushButton(parent)
    self.generateLDAButton.setGeometry(QtCore.QRect(222,140, 88,34))
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
    
    if self.processed_dataframe is not None: 
        self.populate_pca_table()

def run_plot_widget(self):
    if self.processed_dataframe is None:
        QMessageBox.critical(self.window, "Error", "No processed dataframe to be plotted")
        return 
    if 'Predictions' in self.processed_dataframe.columns:
        if len(self.processed_dataframe.columns.tolist()) == 3:
            labels = self.processed_dataframe['Predictions']
            data = self.processed_dataframe.drop(columns=['Predictions'])
            plot_widget = PlotWidget(data, labels=labels)
        elif len(self.processed_dataframe.columns.tolist()) == 4: 
            labels = self.processed_dataframe['Predictions']
            data = self.processed_dataframe.drop(columns=['Predictions'])
            plot_widget = PlotWidget(data, labels=labels, plot_type='3D')
        else:
            QMessageBox.warning(self.window, "Error", f"Not possible to plot with {len(self.processed_dataframe.columns.tolist()) - 1} features")
            return 
    else:
        if len(self.processed_dataframe.columns.tolist()) == 2:
            plot_widget = PlotWidget(self.processed_dataframe)
        elif len(self.processed_dataframe.columns.tolist()) == 3:
            plot_widget = PlotWidget(self.processed_dataframe, plot_type='3D')
        else:
            QMessageBox.warning(self.window, "Error", f"Not possible to plot with {len(self.processed_dataframe.columns.tolist()) - 1} features")
            return 
    plot_widget.exec_()


def generate_LDA_information(self):
    target = self.targetColCB.currentText()
    dataframe = self.current_dataframe.copy()
    num_components = self.numComponentsInputLDA.text()
    scaler = self.scalerOptions.currentText()

    if num_components == '':
        QMessageBox.warning(self.window, "Invalid value", "Insert a valid number of components")
        return
    elif int(num_components) > len(self.current_dataframe.columns.tolist()) or int(num_components) <= 0:
        QMessageBox.warning(self.window, "Invalid value", "Insert a valid number of components")
        return 
    num_components = int(num_components)

    results, acc, err = apply_lda(dataframe, num_components, scaler, target)

    if err is not None:
        QMessageBox.critical(self.window, "Error", f"{str(err)}")
    else: 
        dataframe['Predictions'] = results
        dataframe = dataframe.drop(columns=[target])
        self.processed_dataframe = dataframe
        self.processed_dataframe_type = "LDA"
        self.accLabel.setText(f"Accuracy: {acc:.4f}")
        self.populate_pca_table()
