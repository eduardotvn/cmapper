from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget
from utils.machineLearning.linearRegressionCLS import apply_lnr
import pickle
from frames.mainframe_features.MachineLearning.DecisionTree.Dialogs.showCM import ConfusionMatrixDialog
from sklearn.linear_model import LinearRegression
from .Dialogs.lnrPlot import LinearRegressionDialog
from frames.buttons.mainFuncs import save_data

def load_LNR_buttons(self, parent):
    self.LNRData = LNR_Data()

    self.defaultDataframeLabel = QtWidgets.QLabel(parent)
    self.defaultDataframeLabel.setGeometry(QtCore.QRect(5, 20, 150, 30))
    self.defaultDataframeLabel.setText("Using current dataframe")

    self.LNRInfoData = QtWidgets.QTextEdit(parent)
    self.LNRInfoData.setGeometry(QtCore.QRect(350, 40, 400, 300))
    self.LNRInfoData.setStyleSheet("border: 1px solid black;")
    
    self.plotRegression = QtWidgets.QPushButton(parent)
    self.plotRegression.setGeometry(QtCore.QRect(665, 380, 88, 34))
    self.plotRegression.setText("Plot LNR")
    self.plotRegression.clicked.connect(lambda: view_lnr(self))
    self.plotRegression.hide()

    self.targetColInputLabel = QtWidgets.QLabel(parent)
    self.targetColInputLabel.setGeometry(QtCore.QRect(5, 90, 150, 30))
    self.targetColInputLabel.setText("Target column:")

    self.targetColInputLNR =  QtWidgets.QComboBox(parent)
    self.targetColInputLNR.setGeometry(QtCore.QRect(160, 90, 150, 30))
    self.targetColInputLNR.addItems(self.current_dataframe.columns.tolist())

    self.testSizeInputLabel = QtWidgets.QLabel(parent)
    self.testSizeInputLabel.setGeometry(QtCore.QRect(5, 140, 150, 30))
    self.testSizeInputLabel.setText("Test Size (%):")

    self.testSizeInputLNR =  QtWidgets.QLineEdit(parent)
    self.testSizeInputLNR.setGeometry(QtCore.QRect(160, 140, 150, 30))

    self.randomStateInputLabel = QtWidgets.QLabel(parent)
    self.randomStateInputLabel.setGeometry(QtCore.QRect(5, 190, 150, 30))
    self.randomStateInputLabel.setText("Random state:")

    self.randomStateInputLNR =  QtWidgets.QLineEdit(parent)
    self.randomStateInputLNR.setGeometry(QtCore.QRect(160, 190, 150, 30))

    self.trainLNRButton = QtWidgets.QPushButton(parent)
    self.trainLNRButton.setGeometry(QtCore.QRect(225, 240, 88, 34))
    self.trainLNRButton.setText("Train")
    self.trainLNRButton.clicked.connect(lambda: run_LNR_training(self))

    self.LNRDefaultValues = QtWidgets.QLabel(parent)
    self.LNRDefaultValues.setGeometry(QtCore.QRect(5, 225, 220, 60))
    self.LNRDefaultValues.setText("Use default values:\n(Random State and Test Size)")
    
    self.LNRDefaultValuesCB = QtWidgets.QCheckBox(parent)
    self.LNRDefaultValuesCB.setGeometry(QtCore.QRect(125, 238, 20, 20))
    self.LNRDefaultValuesCB.stateChanged.connect(lambda: set_default_Values(self))

    self.saveModelButton = QtWidgets.QPushButton(parent)
    self.saveModelButton.setGeometry(QtCore.QRect(225, 340, 88, 34))
    self.saveModelButton.setText("Save Model")
    self.saveModelButton.clicked.connect(lambda: save_LNR_model(self))
    self.saveModelButton.hide()

    self.loadModelButton = QtWidgets.QPushButton(parent)
    self.loadModelButton.setGeometry(QtCore.QRect(5, 375, 88, 34))
    self.loadModelButton.setText("Load Model")
    self.loadModelButton.clicked.connect(lambda: load_LNR_model(self))

    self.loadedModelLabel = QtWidgets.QLabel(parent)
    self.loadedModelLabel.setGeometry(QtCore.QRect(100, 375, 100, 34))
    self.loadedModelLabel.hide()

    self.applyLNRButton = QtWidgets.QPushButton(parent)
    self.applyLNRButton.setGeometry(QtCore.QRect(5, 420, 88, 34))
    self.applyLNRButton.setText("Apply LNR")
    self.applyLNRButton.clicked.connect(lambda: apply_LNR_over_dataset(self))

def set_default_Values(self):
    self.testSizeInputLNR.setText("20")
    self.randomStateInputLNR.setText("42")

def set_LNR_info(self):
    content = f"""Linear Regression Model
This classifier was trained on:
Test Size: {self.testSizeInputLNR.text()}%
Random State: {self.randomStateInputLNR.text()}
On a total of {len(self.current_dataframe.columns) - 1} features.
With metrics:
Minimum Squared Error: {self.LNRData.mse}
R2: {self.LNRData.r2}
Resulting classifier and predictions may be saved.
Weight files can be reused by clicking on "Load CLS" 
"""
    self.LNRInfoData.setText(content)

def run_LNR_training(self):
    dataframe = self.current_dataframe
    target = self.targetColInputLNR.currentText()
    r_state = self.randomStateInputLNR.text()
    test_size = self.testSizeInputLNR.text()

    if r_state == '' or int(r_state) < 0:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid random state")
        return
    if test_size == '' or int(test_size) <= 0 or int(test_size) >= 100:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid test size")
        return 
    
    r_state = int(r_state)
    test_size = int(test_size)

    classifier, mse, r2, X_test, y_test, y_pred, err = apply_lnr(dataframe, target, r_state, test_size)
    if err is not None:
        QMessageBox.critical(self.window, "Error", f"{str(err)}")
        return 
    else: 
        self.LNRData.mse = mse
        self.LNRData.r2 = r2
        self.LNRData.classifier = classifier
        self.LNRData.X_test = X_test
        self.LNRData.y_test = y_test
        self.LNRData.y_pred = y_pred
        set_LNR_info(self)
        self.saveModelButton.show()
        self.plotRegression.show()
        self.viewCMButton.show()

def save_LNR_model(self):

    classifier = self.LNRData.classifier 
    if classifier is None:
        QMessageBox.warning(self, "No Model", "There is no trained model to save.")
        return
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(self.window, 
                                               "Save Decision Tree Model",
                                               "",
                                               "Pickle Files (*.pkl);;All Files (*)",
                                               options=options)
    if file_path:
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(classifier, file)
            QMessageBox.information(self.window, "Success", f"Model saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to save model: {str(e)}")

def load_LNR_model(self):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(self.window,
                                               "Load Decision Tree Model",
                                               "",
                                               "Pickle Files (*.pkl);;All Files (*)",
                                               options=options)
    if file_path:
        try:
            with open(file_path, 'rb') as file:
                classifier = pickle.load(file)
            self.LNRData.classifier = classifier
            QMessageBox.information(self.window, "Success", f"Model loaded from {file_path}")
            self.loadedModelLabel.setText(file_path)
            self.loadedModelLabel.show()
            QMessageBox.warning(self.window, "Important", "Be mindful that models must be used in a dataset with same features as the one it was trained on.")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to load model: {str(e)}")

def view_lnr(self):
    if len(self.current_dataframe.columns.tolist()) > 2:
        QMessageBox.warning(self.window, "Error", "Sorry, at the moment, a dataset with more than 1 non-target feature cannot be plotted")
        return 
    lnrplot = LinearRegressionDialog(self.LNRData.X_test, self.LNRData.y_test, self.LNRData.y_pred)
    lnrplot.exec_()

def apply_LNR_over_dataset(self):
    try:
        if not hasattr(self.LNRData, 'classifier') or self.LNRData.classifier is None:
            raise ValueError("Classifier is not initialized.")
        if not hasattr(self, 'current_dataframe') or self.current_dataframe is None:
            raise ValueError("Current dataframe is not initialized.")
        
        classifier = self.LNRData.classifier
        df = self.current_dataframe.copy()
        
        expected_features = classifier.feature_names_in_
        if not all(feature in df.columns for feature in expected_features):
            raise ValueError("Current dataframe does not contain the expected features.")
        
        predictions = classifier.predict(df[expected_features])
        df['Pred'] = predictions
        self.current_dataframe = df
        
        self.predictedDFInfo = QTableWidget(parent=self.LNRInfoData.parent())
        self.predictedDFInfo.setGeometry(self.LNRInfoData.geometry())
        self.predictedDFInfo.setStyleSheet("border: 1px solid black;")

        self.savePredictedDFButton = QPushButton(parent = self.LNRInfoData.parent())
        self.savePredictedDFButton.setGeometry(self.saveModelButton.geometry())
        self.savePredictedDFButton.clicked.connect(lambda: save_data(self, self.current_dataframe))
        self.savePredictedDFButton.setText("Save DF")
        self.savePredictedDFButton.show()
        
        df = self.current_dataframe
        
        self.predictedDFInfo.setRowCount(df.shape[0])
        self.predictedDFInfo.setColumnCount(df.shape[1])
        
        self.predictedDFInfo.setHorizontalHeaderLabels(df.columns)
        
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                self.predictedDFInfo.setItem(row, col, item)
        self.predictedDFInfo.show()
    except ValueError as ve:
        QMessageBox.critical(self.window, "Value Error", f"{str(ve)}")
    except AttributeError as ae:
        QMessageBox.critical(self.window, "Attribute Error", f"{str(ae)}")
    except Exception as e:
        QMessageBox.critical(self.window, "Error", f"An unexpected error occurred: {str(e)}")


class LNR_Data:

    def __init__(self, r2=None, mse=None, classifier=None, X_test=None, y_test = None, y_pred=None):
        self.mse = mse
        self.r2 = r2
        self.classifier = classifier 
        self.X_test = X_test
        self.y_test = y_test
        self.y_pred = y_pred
