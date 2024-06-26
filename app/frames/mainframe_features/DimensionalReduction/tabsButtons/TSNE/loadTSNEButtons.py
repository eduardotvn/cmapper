from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QCheckBox
from PyQt5.QtWidgets import QTableWidgetItem
from utils.applyTSNE import apply_TSNE
from frames.buttons.mainFuncs import run_save_processed_df
from frames.widgets.DfPlot import PlotWidget

def load_TSNE_buttons(self, parent):
    
    self.numComponentsLabel = QtWidgets.QLabel(parent)
    self.numComponentsLabel.setGeometry(QtCore.QRect(5, 30, 150, 30))
    self.numComponentsLabel.setText("Number of components:")

    self.numComponentsInputTSNE = QtWidgets.QLineEdit(parent)
    self.numComponentsInputTSNE.setGeometry(QtCore.QRect(160, 30, 150, 30))
    
    self.scalerLabel = QtWidgets.QLabel(parent)
    self.scalerLabel.setGeometry(QtCore.QRect(5, 65, 100, 30))
    self.scalerLabel.setText("Scaler:")

    self.scalerOptions = QtWidgets.QComboBox(parent)
    self.scalerOptions.setGeometry(QtCore.QRect(160, 65, 150, 30))
    self.scalerOptions.addItems(["Standard", "MinMax", "MaxAbs"])

    self.randomStateLabel = QtWidgets.QLabel(parent)
    self.randomStateLabel.setGeometry(QtCore.QRect(5, 100, 100, 30))
    self.randomStateLabel.setText("Random State:") 

    self.randomStateInput = QtWidgets.QLineEdit(parent)
    self.randomStateInput.setGeometry(QtCore.QRect(160, 100, 150, 30))

    self.perplexityLabel = QtWidgets.QLabel(parent)
    self.perplexityLabel.setGeometry(QtCore.QRect(5, 135, 100, 30))
    self.perplexityLabel.setText("Perplexity:")

    self.perplexityInput = QtWidgets.QLineEdit(parent)
    self.perplexityInput.setGeometry(QtCore.QRect(160, 135, 150, 30))

    self.numIterationLabel = QtWidgets.QLabel(parent)
    self.numIterationLabel.setGeometry(QtCore.QRect(5, 170, 100, 30))
    self.numIterationLabel.setText("Nº of Iterations:")

    self.numIterationInput = QtWidgets.QLineEdit(parent)
    self.numIterationInput.setGeometry(QtCore.QRect(160, 170, 150, 30))

    self.generateTSNEButton = QtWidgets.QPushButton(parent)
    self.generateTSNEButton.setGeometry(QtCore.QRect(222,240, 88,34))
    self.generateTSNEButton.setText("Generate")
    self.generateTSNEButton.clicked.connect(lambda: generate_TSNE_information(self))

    self.defaultValuesLabel = QtWidgets.QLabel(parent)
    self.defaultValuesLabel.setGeometry(QtCore.QRect(5, 205, 220, 60))
    self.defaultValuesLabel.setText("Use default values:\n(random, perplexity and iterations)")

    self.defaultValuesCB = QtWidgets.QCheckBox(parent)
    self.defaultValuesCB.setGeometry(QtCore.QRect(125, 218, 20, 20))
    self.defaultValuesCB.stateChanged.connect(lambda: load_default_values(self))

    self.TSNEInfoData = QtWidgets.QTableWidget(parent)
    self.TSNEInfoData.setGeometry(QtCore.QRect(350, 30, 400, 200))
    self.TSNEInfoData.setStyleSheet("border: 1px solid black;")

    self.plotButton = QtWidgets.QPushButton(parent)
    self.plotButton.setGeometry(QtCore.QRect(665, 240, 88, 34))
    self.plotButton.setText("Plot")
    self.plotButton.clicked.connect(lambda: run_plot_widget(self))

    self.saveDFButton = QtWidgets.QPushButton(parent)
    self.saveDFButton.setGeometry(QtCore.QRect(565, 240, 88, 34))
    self.saveDFButton.setText("Save DF")
    self.saveDFButton.clicked.connect(lambda: run_save_processed_df(self))

    if self.current_dataframe_type is not None: 
        self.populate_pca_table()


def generate_TSNE_information(self):
    try:
        num_components = self.numComponentsInputTSNE.text()
        if not num_components.isdigit() or num_components == '' or int(num_components) <= 0 or int(num_components) > len(self.current_dataframe.columns.tolist()):
            QMessageBox.warning(self.window, "Value Error", "Enter a valid value for number of components")
            return 

        scaler = self.scalerOptions.currentText()

        rand_state = self.randomStateInput.text()

        if not rand_state.isdigit() or rand_state == '' or int(rand_state) < 0:
            QMessageBox.warning(self.window, "Value Error", "Enter a valid value for number for random state")
            return 

        perplexity = self.perplexityInput.text()

        if not perplexity.isdigit() or perplexity == '' or int(perplexity) < 0:
            QMessageBox.warning(self.window, "Value Error", "Enter a valid value for perplexity")
            return

        iterations = self.numIterationInput.text()
        if not iterations.isdigit() or iterations == '' or int(perplexity) < 0:
            QMessageBox.warning(self.window, "Value Error", "Enter a valid value for number of iterations")
            return 
        
        num_components = int(num_components)
        rand_state = int(rand_state)
        perplexity = int(perplexity)
        iterations = int(iterations)

        resulting_df, error = apply_TSNE(self.current_dataframe, num_components, scaler, rand_state, perplexity, iterations)

        if resulting_df is not None: 
            self.current_dataframe = resulting_df
            self.current_dataframe_type = "TSNE"
            self.populate_pca_table()
        else:
            QMessageBox.critical(self.window, "Error", f"{str(error)}")
    except Exception as e:
        QMessageBox.critical(self.window, "Error", f"{str(e)}")
    

def load_default_values(self):
    self.randomStateInput.setText("0")
    self.perplexityInput.setText("30")
    self.numIterationInput.setText("300")

def run_plot_widget(self):
    if self.current_dataframe is None:
        QMessageBox.critical(self.window, "Error", "No processed dataframe to be plotted")
        return 
    if len(self.current_dataframe.columns.tolist()) == 2:
        plot_widget = PlotWidget(self.current_dataframe)
    elif len(self.current_dataframe.columns.tolist()) == 3:
        plot_widget = PlotWidget(self.current_dataframe, plot_type='3D')
    else:
        QMessageBox.warning(self.window, "Error", f"Not possible to plot with {len(self.current_dataframe.columns.tolist()) - 1} features")
        return 
    plot_widget.exec_()