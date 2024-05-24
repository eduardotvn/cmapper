from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget, QPushButton
from utils.machineLearning.logisticRegressionCLS import apply_lgr
import pickle
from frames.mainframe_features.MachineLearning.DecisionTree.Dialogs.showCM import ConfusionMatrixDialog
from sklearn.linear_model import LinearRegression
from frames.buttons.mainFuncs import save_data
from frames.mainframe_features.DataframeEdit.Dialogs.DataFrameHead import DataFrameDialog

def load_LGR_buttons(self, parent):
    self.LGRData = LGR_Data()

    self.defaultDataframeLabel = QtWidgets.QLabel(parent)
    self.defaultDataframeLabel.setGeometry(QtCore.QRect(5, 20, 150, 30))
    self.defaultDataframeLabel.setText("Using current dataframe")

    self.defaultDataframePreviewLGR = QtWidgets.QPushButton(parent)
    self.defaultDataframePreviewLGR.setGeometry(QtCore.QRect(160, 20, 88, 34))
    self.defaultDataframePreviewLGR.setText("Preview")
    self.defaultDataframePreviewLGR.clicked.connect(lambda: show_dataframe_sample(self))

    self.LGRInfoData = QtWidgets.QTextEdit(parent)
    self.LGRInfoData.setGeometry(QtCore.QRect(350, 40, 400, 300))
    self.LGRInfoData.setStyleSheet("border: 1px solid black;")
    
    self.viewCMButtonLGR = QtWidgets.QPushButton(parent)
    self.viewCMButtonLGR.setGeometry(QtCore.QRect(565, 380, 88, 34))
    self.viewCMButtonLGR.setText("View CM")
    self.viewCMButtonLGR.clicked.connect(lambda: view_confusion_matrix(self))
    self.viewCMButtonLGR.hide()

    self.targetColInputLabel = QtWidgets.QLabel(parent)
    self.targetColInputLabel.setGeometry(QtCore.QRect(5, 90, 150, 30))
    self.targetColInputLabel.setText("Target column:")

    self.targetColInputLGR =  QtWidgets.QComboBox(parent)
    self.targetColInputLGR.setGeometry(QtCore.QRect(160, 90, 150, 30))
    self.targetColInputLGR.addItems(self.current_dataframe.columns.tolist())

    self.testSizeInputLabel = QtWidgets.QLabel(parent)
    self.testSizeInputLabel.setGeometry(QtCore.QRect(5, 140, 150, 30))
    self.testSizeInputLabel.setText("Test Size (%):")

    self.testSizeInputLGR =  QtWidgets.QLineEdit(parent)
    self.testSizeInputLGR.setGeometry(QtCore.QRect(160, 140, 150, 30))

    self.randomStateInputLabel = QtWidgets.QLabel(parent)
    self.randomStateInputLabel.setGeometry(QtCore.QRect(5, 190, 150, 30))
    self.randomStateInputLabel.setText("Random state:")

    self.randomStateInputLGR =  QtWidgets.QLineEdit(parent)
    self.randomStateInputLGR.setGeometry(QtCore.QRect(160, 190, 150, 30))

    self.trainLGRButton = QtWidgets.QPushButton(parent)
    self.trainLGRButton.setGeometry(QtCore.QRect(225, 240, 88, 34))
    self.trainLGRButton.setText("Train")
    self.trainLGRButton.clicked.connect(lambda: run_LGR_training(self))

    self.LGRDefaultValues = QtWidgets.QLabel(parent)
    self.LGRDefaultValues.setGeometry(QtCore.QRect(5, 225, 220, 60))
    self.LGRDefaultValues.setText("Use default values:\n(Random State and Test Size)")
    
    self.LGRDefaultValuesCB = QtWidgets.QCheckBox(parent)
    self.LGRDefaultValuesCB.setGeometry(QtCore.QRect(125, 238, 20, 20))
    self.LGRDefaultValuesCB.stateChanged.connect(lambda: set_default_Values(self))

    self.saveModelButtonLGR = QtWidgets.QPushButton(parent)
    self.saveModelButtonLGR.setGeometry(QtCore.QRect(225, 340, 88, 34))
    self.saveModelButtonLGR.setText("Save Model")
    self.saveModelButtonLGR.clicked.connect(lambda: save_LGR_model(self))
    self.saveModelButtonLGR.hide()

    self.loadModelButton = QtWidgets.QPushButton(parent)
    self.loadModelButton.setGeometry(QtCore.QRect(5, 375, 88, 34))
    self.loadModelButton.setText("Load Model")
    self.loadModelButton.clicked.connect(lambda: load_LGR_model(self))

    self.loadedModelLabelLGR = QtWidgets.QLabel(parent)
    self.loadedModelLabelLGR.setGeometry(QtCore.QRect(100, 375, 100, 34))
    self.loadedModelLabelLGR.hide()

    self.applyLGRButton = QtWidgets.QPushButton(parent)
    self.applyLGRButton.setGeometry(QtCore.QRect(5, 420, 88, 34))
    self.applyLGRButton.setText("Apply LGR")
    self.applyLGRButton.clicked.connect(lambda: apply_LGR_over_dataset(self))

def set_default_Values(self):
    self.testSizeInputLGR.setText("20")
    self.randomStateInputLGR.setText("42")

def set_LGR_info(self):
    content = f"""Logistic Regression Model
This classifier was trained on:
Test Size: {self.testSizeInputLGR.text()}%
Random State: {self.randomStateInputLGR.text()}
On a total of {len(self.current_dataframe.columns) - 1} features.
With metrics:
Accuracy: {self.LGRData.accuracy}
Resulting classifier and predictions may be saved.
Weight files can be reused by clicking on "Load CLS" 
Classification Report:
{self.LGRData.report}
"""
    self.LGRInfoData.setText(content)

def run_LGR_training(self):
    dataframe = self.current_dataframe
    target = self.targetColInputLGR.currentText()
    r_state = self.randomStateInputLGR.text()
    test_size = self.testSizeInputLGR.text()

    if r_state == '' or int(r_state) < 0:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid random state")
        return
    if test_size == '' or int(test_size) <= 0 or int(test_size) >= 100:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid test size")
        return 
    
    r_state = int(r_state)
    test_size = int(test_size)

    classifier, accuracy, confusion_matrix, report, err = apply_lgr(dataframe, target, r_state, test_size)
    if err is not None:
        QMessageBox.critical(self.window, "Error", f"{str(err)}")
        return 
    else: 
        self.LGRData.accuracy = accuracy
        self.LGRData.confusion_matrix = confusion_matrix
        self.LGRData.classifier = classifier
        self.LGRData.report = report
        set_LGR_info(self)
        self.saveModelButtonLGR.show()
        self.viewCMButtonLGR.show()

def show_dataframe_sample(self):
    df_sample = self.current_dataframe.head()
    self.dialog = DataFrameDialog(df_sample)
    self.dialog.exec_()

def save_LGR_model(self):

    classifier = self.LGRData.classifier 
    if classifier is None:
        QMessageBox.warning(self, "No Model", "There is no trained model to save.")
        return
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(self.window, 
                                               "Save Logistic Regression Model",
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

def load_LGR_model(self):
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
            self.LGRData.classifier = classifier
            QMessageBox.information(self.window, "Success", f"Model loaded from {file_path}")
            self.loadedModelLabelLGR.setText(file_path)
            self.loadedModelLabelLGR.show()
            QMessageBox.warning(self.window, "Important", "Be mindful that models must be used in a dataset with same features as the one it was trained on.")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to load model: {str(e)}")

def view_confusion_matrix(self):
    cmDialog = ConfusionMatrixDialog(self.SVMData.confusion_matrix)
    cmDialog.exec_()

def apply_LGR_over_dataset(self):
    try:
        if not hasattr(self.LGRData, 'classifier') or self.LGRData.classifier is None:
            raise ValueError("Classifier is not initialized.")
        if not hasattr(self, 'current_dataframe') or self.current_dataframe is None:
            raise ValueError("Current dataframe is not initialized.")
        
        classifier = self.LGRData.classifier
        df = self.current_dataframe.copy()
        
        expected_features = classifier.feature_names_in_
        if not all(feature in df.columns for feature in expected_features):
            raise ValueError("Current dataframe does not contain the expected features.")
        
        predictions = classifier.predict(df[expected_features])
        df['Pred'] = predictions
        self.current_dataframe = df
        
        self.predictedDFInfo = QTableWidget(parent=self.LGRInfoData.parent())
        self.predictedDFInfo.setGeometry(self.LGRInfoData.geometry())
        self.predictedDFInfo.setStyleSheet("border: 1px solid black;")

        self.savePredictedDFButtonLGR = QPushButton(parent = self.LGRInfoData.parent())
        self.savePredictedDFButtonLGR.setGeometry(self.saveModelButtonLGR.geometry())
        self.savePredictedDFButtonLGR.clicked.connect(lambda: save_data(self, self.current_dataframe))
        self.savePredictedDFButtonLGR.setText("Save DF")
        self.savePredictedDFButtonLGR.show()
        
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


class LGR_Data:

    def __init__(self, confusion_matrix=None, accuracy=None, classifier=None, report=None):
        self.accuracy = accuracy
        self.confusion_matrix = confusion_matrix
        self.classifier = classifier 
        self.report = report

