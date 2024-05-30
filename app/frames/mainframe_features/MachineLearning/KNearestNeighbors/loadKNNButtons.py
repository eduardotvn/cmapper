from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget, QPushButton
from utils.machineLearning.knearestNeighboursCLS import apply_knn
import pickle
from frames.mainframe_features.MachineLearning.DecisionTree.Dialogs.showCM import ConfusionMatrixDialog
from frames.buttons.mainFuncs import save_data
from frames.mainframe_features.DataframeEdit.Dialogs.DataFrameHead import DataFrameDialog

def load_KNN_buttons(self, parent):
    self.KNNData = KNN_Data()

    self.defaultDataframeLabel = QtWidgets.QLabel(parent)
    self.defaultDataframeLabel.setGeometry(QtCore.QRect(5, 20, 150, 30))
    self.defaultDataframeLabel.setText("Using current dataframe")

    self.defaultDataframePreviewKNN = QtWidgets.QPushButton(parent)
    self.defaultDataframePreviewKNN.setGeometry(QtCore.QRect(160, 20, 88, 34))
    self.defaultDataframePreviewKNN.setText("Preview")
    self.defaultDataframePreviewKNN.clicked.connect(lambda: show_dataframe_sample(self))

    self.KNNInfoData = QtWidgets.QTextEdit(parent)
    self.KNNInfoData.setGeometry(QtCore.QRect(350, 40, 400, 300))
    self.KNNInfoData.setStyleSheet("border: 1px solid black;")
    
    self.viewCMButtonKNN = QtWidgets.QPushButton(parent)
    self.viewCMButtonKNN.setGeometry(QtCore.QRect(665, 380, 88, 34))
    self.viewCMButtonKNN.setText("View CM")
    self.viewCMButtonKNN.clicked.connect(lambda: view_confusion_matrix(self))
    self.viewCMButtonKNN.hide()

    self.targetColInputLabel = QtWidgets.QLabel(parent)
    self.targetColInputLabel.setGeometry(QtCore.QRect(5, 90, 150, 30))
    self.targetColInputLabel.setText("Target column:")

    self.targetColInputKNN =  QtWidgets.QComboBox(parent)
    self.targetColInputKNN.setGeometry(QtCore.QRect(160, 90, 150, 30))
    self.targetColInputKNN.addItems(self.current_dataframe.columns.tolist())

    self.testSizeInputLabel = QtWidgets.QLabel(parent)
    self.testSizeInputLabel.setGeometry(QtCore.QRect(5, 140, 150, 30))
    self.testSizeInputLabel.setText("Test Size (%):")

    self.testSizeInputKNN =  QtWidgets.QLineEdit(parent)
    self.testSizeInputKNN.setGeometry(QtCore.QRect(160, 140, 150, 30))

    self.randomStateInputLabel = QtWidgets.QLabel(parent)
    self.randomStateInputLabel.setGeometry(QtCore.QRect(5, 190, 150, 30))
    self.randomStateInputLabel.setText("Random state:")

    self.randomStateInputKNN =  QtWidgets.QLineEdit(parent)
    self.randomStateInputKNN.setGeometry(QtCore.QRect(160, 190, 150, 30))

    self.numNeighborsInputLabel = QtWidgets.QLabel(parent)
    self.numNeighborsInputLabel.setGeometry(QtCore.QRect(5, 240, 150, 30))
    self.numNeighborsInputLabel.setText("Number of neighbors:")

    self.numNeighborsInputKNN =  QtWidgets.QLineEdit(parent)
    self.numNeighborsInputKNN.setGeometry(QtCore.QRect(160, 240, 150, 30))

    self.trainKNNButton = QtWidgets.QPushButton(parent)
    self.trainKNNButton.setGeometry(QtCore.QRect(225, 275, 88, 34))
    self.trainKNNButton.setText("Train")
    self.trainKNNButton.clicked.connect(lambda: run_KNN_training(self))

    self.KNNDefaultValues = QtWidgets.QLabel(parent)
    self.KNNDefaultValues.setGeometry(QtCore.QRect(5, 275, 220, 60))
    self.KNNDefaultValues.setText("Use default values:\n(Random State and Test Size)")
    
    self.KNNDefaultValuesCB = QtWidgets.QCheckBox(parent)
    self.KNNDefaultValuesCB.setGeometry(QtCore.QRect(125, 288, 20, 20))
    self.KNNDefaultValuesCB.stateChanged.connect(lambda: set_default_Values(self))

    self.saveModelButtonKNN = QtWidgets.QPushButton(parent)
    self.saveModelButtonKNN.setGeometry(QtCore.QRect(225, 340, 88, 34))
    self.saveModelButtonKNN.setText("Save Model")
    self.saveModelButtonKNN.clicked.connect(lambda: save_KNN_model(self))
    self.saveModelButtonKNN.hide()

    self.loadModelButton = QtWidgets.QPushButton(parent)
    self.loadModelButton.setGeometry(QtCore.QRect(5, 375, 88, 34))
    self.loadModelButton.setText("Load Model")
    self.loadModelButton.clicked.connect(lambda: load_KNN_model(self))

    self.loadedModelLabelKNN = QtWidgets.QLabel(parent)
    self.loadedModelLabelKNN.setGeometry(QtCore.QRect(100, 375, 100, 34))
    self.loadedModelLabelKNN.hide()

    self.applyKNNButton = QtWidgets.QPushButton(parent)
    self.applyKNNButton.setGeometry(QtCore.QRect(5, 420, 88, 34))
    self.applyKNNButton.setText("Apply KNN")
    self.applyKNNButton.clicked.connect(lambda: apply_KNN_over_dataset(self))

def set_default_Values(self):
    self.testSizeInputKNN.setText("20")
    self.randomStateInputKNN.setText("42")
    self.numNeighborsInputKNN.setText("3")

def set_KNN_info(self):
    content = f"""K-Nearest Neighbors Model
This classifier was trained on:
Test Size: {self.testSizeInputKNN.text()}%
Random State: {self.randomStateInputKNN.text()}
On a total of {len(self.current_dataframe.columns) - 1} features.
With metrics:
Accuracy: {self.KNNData.accuracy}
Resulting classifier and predictions may be saved.
Weight files can be reused by clicking on "Load CLS" 
Classification Report:
{self.KNNData.class_report}
"""
    self.KNNInfoData.setText(content)

def run_KNN_training(self):
    dataframe = self.current_dataframe
    target = self.targetColInputKNN.currentText()
    r_state = self.randomStateInputKNN.text()
    test_size = self.testSizeInputKNN.text()
    numNeighbors = self.numNeighborsInputKNN.text()

    if not r_state.isdigit() or r_state == '' or int(r_state) < 0:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid random state")
        return
    if not test_size.isdigit() or test_size == '' or int(test_size) <= 0 or int(test_size) >= 100:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid test size")
        return 
    if not numNeighbors.isdigit() or numNeighbors == '':
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid neighbors number")
        return         

    r_state = int(r_state)
    test_size = int(test_size)
    numNeighbors = int(numNeighbors)

    classifier, accuracy, cls_report, conf_matrix, err = apply_knn(dataframe, target, r_state, test_size, numNeighbors)
    if err is not None:
        QMessageBox.critical(self.window, "Error", f"{str(err)}")
        return 
    else: 
        self.KNNData.accuracy = accuracy
        self.KNNData.classifier = classifier
        self.KNNData.class_report = cls_report
        self.KNNData.confusion_matrix = conf_matrix
        set_KNN_info(self)
        self.saveModelButtonKNN.show()
        self.viewTreeButton.show()
        self.viewCMButtonKNN.show()

def save_KNN_model(self):

    classifier = self.KNNData.classifier 
    if classifier is None:
        QMessageBox.warning(self, "No Model", "There is no trained model to save.")
        return
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getSaveFileName(self.window, 
                                               "Save KNN Model",
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

def load_KNN_model(self):
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
            self.KNNData.classifier = classifier
            QMessageBox.information(self.window, "Success", f"Model loaded from {file_path}")
            self.loadedModelLabelKNN.setText(file_path)
            self.loadedModelLabelKNN.show()
            QMessageBox.warning(self.window, "Important", "Be mindful that models must be used in a dataset with same features as the one it was trained on.")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to load model: {str(e)}")

def view_confusion_matrix(self):
    cmDialog = ConfusionMatrixDialog(self.KNNData.confusion_matrix)
    cmDialog.exec_()

def show_dataframe_sample(self):
    df_sample = self.current_dataframe.head()
    self.dialog = DataFrameDialog(df_sample)
    self.dialog.exec_()

def apply_KNN_over_dataset(self):
    try:
        if not hasattr(self.KNNData, 'classifier') or self.KNNData.classifier is None:
            raise ValueError("Classifier is not initialized.")
        if not hasattr(self, 'current_dataframe') or self.current_dataframe is None:
            raise ValueError("Current dataframe is not initialized.")
        
        classifier = self.KNNData.classifier
        df = self.current_dataframe.copy()
        
        expected_features = classifier.feature_names_in_
        if not all(feature in df.columns for feature in expected_features):
            raise ValueError("Current dataframe does not contain the expected features.")
        
        predictions = classifier.predict(df[expected_features])
        df['Pred'] = predictions
        self.current_dataframe = df
        
        self.predictedDFInfo = QTableWidget(parent=self.KNNInfoData.parent())
        self.predictedDFInfo.setGeometry(self.KNNInfoData.geometry())
        self.predictedDFInfo.setStyleSheet("border: 1px solid black;")

        self.savePredictedDFButtonKNN = QPushButton(parent = self.KNNInfoData.parent())
        self.savePredictedDFButtonKNN.setGeometry(self.saveModelButtonKNN.geometry())
        self.savePredictedDFButtonKNN.clicked.connect(lambda: save_data(self, self.current_dataframe))
        self.savePredictedDFButtonKNN.setText("Save DF")
        self.savePredictedDFButtonKNN.show()
        
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


class KNN_Data:
    def __init__(self, accuracy=None, classifier=None, classification_report=None, confusion_matrix = None):
        self.accuracy = accuracy
        self.classifier = classifier 
        self.class_report = classification_report
        self.confusion_matrix = confusion_matrix
