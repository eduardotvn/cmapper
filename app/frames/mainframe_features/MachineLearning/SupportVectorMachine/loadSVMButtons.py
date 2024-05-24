from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget
from utils.machineLearning.supportVectorMachineCLS import apply_svm
import pickle
from frames.mainframe_features.MachineLearning.DecisionTree.Dialogs.showCM import ConfusionMatrixDialog
from sklearn.linear_model import LinearRegression
from frames.buttons.mainFuncs import save_data

def load_SVM_buttons(self, parent):
    self.SVMData = SVM_Data()

    self.defaultDataframeLabel = QtWidgets.QLabel(parent)
    self.defaultDataframeLabel.setGeometry(QtCore.QRect(5, 20, 150, 30))
    self.defaultDataframeLabel.setText("Using current dataframe")

    self.SVMInfoData = QtWidgets.QTextEdit(parent)
    self.SVMInfoData.setGeometry(QtCore.QRect(350, 40, 400, 300))
    self.SVMInfoData.setStyleSheet("border: 1px solid black;")
    
    self.viewCMButtonSVM = QtWidgets.QPushButton(parent)
    self.viewCMButtonSVM.setGeometry(QtCore.QRect(665, 380, 88, 34))
    self.viewCMButtonSVM.setText("View CM")
    self.viewCMButtonSVM.clicked.connect(lambda: view_confusion_matrix(self))
    self.viewCMButtonSVM.hide()

    self.targetColInputLabel = QtWidgets.QLabel(parent)
    self.targetColInputLabel.setGeometry(QtCore.QRect(5, 90, 150, 30))
    self.targetColInputLabel.setText("Target column:")

    self.targetColInputSVM =  QtWidgets.QComboBox(parent)
    self.targetColInputSVM.setGeometry(QtCore.QRect(160, 90, 150, 30))
    self.targetColInputSVM.addItems(self.current_dataframe.columns.tolist())

    self.testSizeInputLabel = QtWidgets.QLabel(parent)
    self.testSizeInputLabel.setGeometry(QtCore.QRect(5, 140, 150, 30))
    self.testSizeInputLabel.setText("Test Size (%):")

    self.testSizeInputSVM =  QtWidgets.QLineEdit(parent)
    self.testSizeInputSVM.setGeometry(QtCore.QRect(160, 140, 150, 30))

    self.randomStateInputLabel = QtWidgets.QLabel(parent)
    self.randomStateInputLabel.setGeometry(QtCore.QRect(5, 190, 150, 30))
    self.randomStateInputLabel.setText("Random state:")

    self.randomStateInputSVM =  QtWidgets.QLineEdit(parent)
    self.randomStateInputSVM.setGeometry(QtCore.QRect(160, 190, 150, 30))

    self.trainSVMButton = QtWidgets.QPushButton(parent)
    self.trainSVMButton.setGeometry(QtCore.QRect(225, 240, 88, 34))
    self.trainSVMButton.setText("Train")
    self.trainSVMButton.clicked.connect(lambda: run_SVM_training(self))

    self.SVMDefaultValues = QtWidgets.QLabel(parent)
    self.SVMDefaultValues.setGeometry(QtCore.QRect(5, 225, 220, 60))
    self.SVMDefaultValues.setText("Use default values:\n(Random State and Test Size)")
    
    self.SVMDefaultValuesCB = QtWidgets.QCheckBox(parent)
    self.SVMDefaultValuesCB.setGeometry(QtCore.QRect(125, 238, 20, 20))
    self.SVMDefaultValuesCB.stateChanged.connect(lambda: set_default_Values(self))

    self.saveModelButton = QtWidgets.QPushButton(parent)
    self.saveModelButton.setGeometry(QtCore.QRect(225, 340, 88, 34))
    self.saveModelButton.setText("Save Model")
    self.saveModelButton.clicked.connect(lambda: save_SVM_model(self))
    self.saveModelButton.hide()

    self.loadModelButton = QtWidgets.QPushButton(parent)
    self.loadModelButton.setGeometry(QtCore.QRect(5, 375, 88, 34))
    self.loadModelButton.setText("Load Model")
    self.loadModelButton.clicked.connect(lambda: load_SVM_model(self))

    self.loadedModelLabel = QtWidgets.QLabel(parent)
    self.loadedModelLabel.setGeometry(QtCore.QRect(100, 375, 100, 34))
    self.loadedModelLabel.hide()

    self.applySVMButton = QtWidgets.QPushButton(parent)
    self.applySVMButton.setGeometry(QtCore.QRect(5, 420, 88, 34))
    self.applySVMButton.setText("Apply SVM")
    self.applySVMButton.clicked.connect(lambda: apply_SVM_over_dataset(self))

def set_default_Values(self):
    self.testSizeInputSVM.setText("20")
    self.randomStateInputSVM.setText("42")

def set_SVM_info(self):
    content = f"""Support Vector Machine Model
This classifier was trained on:
Test Size: {self.testSizeInputSVM.text()}%
Random State: {self.randomStateInputSVM.text()}
On a total of {len(self.current_dataframe.columns) - 1} features.
With metrics:
Accuracy: {self.SVMData.accuracy}
Resulting classifier and predictions may be saved.
Weight files can be reused by clicking on "Load CLS" 
Classification Report: 
f{self.SVMData.report}
"""
    self.SVMInfoData.setText(content)

def run_SVM_training(self):
    dataframe = self.current_dataframe
    target = self.targetColInputSVM.currentText()
    r_state = self.randomStateInputSVM.text()
    test_size = self.testSizeInputSVM.text()

    if r_state == '' or int(r_state) < 0:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid random state")
        return
    if test_size == '' or int(test_size) <= 0 or int(test_size) >= 100:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid test size")
        return 
    
    r_state = int(r_state)
    test_size = int(test_size)

    classifier, accuracy, confusion_matrix, class_report, err = apply_svm(dataframe, target, r_state, test_size)
    if err is not None:
        QMessageBox.critical(self.window, "Error", f"{str(err)}")
        return 
    else: 
        self.SVMData.accuracy = accuracy
        self.SVMData.confusion_matrix = confusion_matrix
        self.SVMData.classifier = classifier
        self.SVMData.report = class_report
        set_SVM_info(self)
        self.saveModelButton.show()
        self.viewCMButtonSVM.show()

def save_SVM_model(self):

    classifier = self.SVMData.classifier 
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

def view_confusion_matrix(self):
    cmDialog = ConfusionMatrixDialog(self.SVMData.confusion_matrix)
    cmDialog.exec_()

def load_SVM_model(self):
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
            self.SVMData.classifier = classifier
            QMessageBox.information(self.window, "Success", f"Model loaded from {file_path}")
            self.loadedModelLabel.setText(file_path)
            self.loadedModelLabel.show()
            QMessageBox.warning(self.window, "Important", "Be mindful that models must be used in a dataset with same features as the one it was trained on.")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to load model: {str(e)}")

def view_SVM(self):
    if len(self.current_dataframe.columns.tolist()) > 2:
        QMessageBox.warning(self.window, "Error", "Sorry, at the moment, a dataset with more than 1 non-target feature cannot be plotted")
        return 
    SVMplot = LinearRegressionDialog(self.SVMData.X_test, self.SVMData.y_test, self.SVMData.y_pred)
    SVMplot.exec_()

def apply_SVM_over_dataset(self):
    try:
        if not hasattr(self.SVMData, 'classifier') or self.SVMData.classifier is None:
            raise ValueError("Classifier is not initialized.")
        if not hasattr(self, 'current_dataframe') or self.current_dataframe is None:
            raise ValueError("Current dataframe is not initialized.")
        
        classifier = self.SVMData.classifier
        df = self.current_dataframe.copy()
        
        expected_features = classifier.feature_names_in_
        if not all(feature in df.columns for feature in expected_features):
            raise ValueError("Current dataframe does not contain the expected features.")
        
        predictions = classifier.predict(df[expected_features])
        df['Pred'] = predictions
        self.current_dataframe = df
        
        self.predictedDFInfo = QTableWidget(parent=self.SVMInfoData.parent())
        self.predictedDFInfo.setGeometry(self.SVMInfoData.geometry())
        self.predictedDFInfo.setStyleSheet("border: 1px solid black;")

        self.savePredictedDFButton = QPushButton(parent = self.SVMInfoData.parent())
        self.savePredictedDFButton.setGeometry(self.saveModelButton.geometry())
        self.savePredictedDFButton.clicked.connect(lambda: save_data(self, self.current_dataframe))
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


class SVM_Data:

    def __init__(self, report=None, accuracy=None, classifier=None, confusion_matrix=None):
        self.accuracy = accuracy
        self.report = report
        self.classifier = classifier 
        self.confusion_matrix = confusion_matrix
