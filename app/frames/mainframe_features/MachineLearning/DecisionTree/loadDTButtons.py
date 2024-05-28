from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget, QPushButton
from utils.machineLearning.decisionTreeCLS import apply_dt
import pickle
from frames.mainframe_features.MachineLearning.DecisionTree.Dialogs.showDT import DecisionTreeDialog
from frames.mainframe_features.MachineLearning.DecisionTree.Dialogs.showCM import ConfusionMatrixDialog
from sklearn.tree import DecisionTreeClassifier
from frames.buttons.mainFuncs import save_data
from frames.mainframe_features.DataframeEdit.Dialogs.DataFrameHead import DataFrameDialog

def load_dt_buttons(self, parent):
    self.DTData = DT_Data()

    self.defaultDataframeLabel = QtWidgets.QLabel(parent)
    self.defaultDataframeLabel.setGeometry(QtCore.QRect(5, 20, 150, 30))
    self.defaultDataframeLabel.setText("Using current dataframe")

    self.defaultDataframePreviewDT = QtWidgets.QPushButton(parent)
    self.defaultDataframePreviewDT.setGeometry(QtCore.QRect(160, 20, 88, 34))
    self.defaultDataframePreviewDT.setText("Preview")
    self.defaultDataframePreviewDT.clicked.connect(lambda: show_dataframe_sample(self))

    self.dtInfoData = QtWidgets.QTextEdit(parent)
    self.dtInfoData.setGeometry(QtCore.QRect(350, 40, 400, 300))
    self.dtInfoData.setStyleSheet("border: 1px solid black;")
    
    self.viewTreeButton = QtWidgets.QPushButton(parent)
    self.viewTreeButton.setGeometry(QtCore.QRect(665, 380, 88, 34))
    self.viewTreeButton.setText("View Tree")
    self.viewTreeButton.clicked.connect(lambda: view_tree(self))
    self.viewTreeButton.hide()

    self.viewCMButton = QtWidgets.QPushButton(parent)
    self.viewCMButton.setGeometry(QtCore.QRect(565, 380, 88, 34))
    self.viewCMButton.setText("View CM")
    self.viewCMButton.clicked.connect(lambda: view_confusion_matrix(self))
    self.viewCMButton.hide()

    self.targetColInputLabel = QtWidgets.QLabel(parent)
    self.targetColInputLabel.setGeometry(QtCore.QRect(5, 90, 150, 30))
    self.targetColInputLabel.setText("Target column:")

    self.targetColInputDT =  QtWidgets.QComboBox(parent)
    self.targetColInputDT.setGeometry(QtCore.QRect(160, 90, 150, 30))
    self.targetColInputDT.addItems(self.current_dataframe.columns.tolist())

    self.testSizeInputLabel = QtWidgets.QLabel(parent)
    self.testSizeInputLabel.setGeometry(QtCore.QRect(5, 140, 150, 30))
    self.testSizeInputLabel.setText("Test Size (%):")

    self.testSizeInputDT =  QtWidgets.QLineEdit(parent)
    self.testSizeInputDT.setGeometry(QtCore.QRect(160, 140, 150, 30))

    self.randomStateInputLabel = QtWidgets.QLabel(parent)
    self.randomStateInputLabel.setGeometry(QtCore.QRect(5, 190, 150, 30))
    self.randomStateInputLabel.setText("Random state:")

    self.randomStateInputDT =  QtWidgets.QLineEdit(parent)
    self.randomStateInputDT.setGeometry(QtCore.QRect(160, 190, 150, 30))

    self.trainDTButton = QtWidgets.QPushButton(parent)
    self.trainDTButton.setGeometry(QtCore.QRect(225, 240, 88, 34))
    self.trainDTButton.setText("Train")
    self.trainDTButton.clicked.connect(lambda: run_dt_training(self))

    self.DTDefaultValues = QtWidgets.QLabel(parent)
    self.DTDefaultValues.setGeometry(QtCore.QRect(5, 225, 220, 60))
    self.DTDefaultValues.setText("Use default values:\n(Random State and Test Size)")
    
    self.DTDefaultValuesCB = QtWidgets.QCheckBox(parent)
    self.DTDefaultValuesCB.setGeometry(QtCore.QRect(125, 238, 20, 20))
    self.DTDefaultValuesCB.stateChanged.connect(lambda: set_default_Values(self))

    self.saveModelButtonDT = QtWidgets.QPushButton(parent)
    self.saveModelButtonDT.setGeometry(QtCore.QRect(225, 340, 88, 34))
    self.saveModelButtonDT.setText("Save Model")
    self.saveModelButtonDT.clicked.connect(lambda: save_dt_model(self))
    self.saveModelButtonDT.hide()

    self.loadModelButton = QtWidgets.QPushButton(parent)
    self.loadModelButton.setGeometry(QtCore.QRect(5, 375, 88, 34))
    self.loadModelButton.setText("Load Model")
    self.loadModelButton.clicked.connect(lambda: load_dt_model(self))

    self.loadedModelLabelDT = QtWidgets.QLabel(parent)
    self.loadedModelLabelDT.setGeometry(QtCore.QRect(100, 375, 100, 34))
    self.loadedModelLabelDT.hide()

    self.applyDTButton = QtWidgets.QPushButton(parent)
    self.applyDTButton.setGeometry(QtCore.QRect(5, 420, 88, 34))
    self.applyDTButton.setText("Apply DT")
    self.applyDTButton.clicked.connect(lambda: apply_dt_over_dataset(self))

def set_default_Values(self):
    self.testSizeInputDT.setText("20")
    self.randomStateInputDT.setText("42")

def set_dt_info(self):
    content = f"""Decision Tree Classifier
This classifier was trained on:
Test Size: {self.testSizeInputDT.text()}%
Random State: {self.randomStateInputDT.text()}
On a total of {len(self.current_dataframe.columns) - 1} features.
With metrics:
Accuracy: {self.DTData.accuracy}
F1-Score: {self.DTData.f1score}
Resulting classifier and predictions may be saved.
Weight files can be reused by clicking on "Load CLS" 
Classification Report:
{self.DTData.class_report}
"""
    self.dtInfoData.setText(content)

def run_dt_training(self):
    dataframe = self.current_dataframe
    target = self.targetColInputDT.currentText()
    r_state = self.randomStateInputDT.text()
    test_size = self.testSizeInputDT.text()

    if not r_state.isdigit() or int(r_state) < 0:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid random state")
        return

    if not test_size.isdigit() or int(test_size) <= 0 or int(test_size) >= 100:
        QMessageBox.warning(self.window, "Invalid Value", "Input a valid test size")
        return

    r_state = int(r_state)
    test_size = int(test_size)

    classifier, accuracy, f1score, cls_report, gini, conf_matrix, err = apply_dt(dataframe, target, r_state, test_size)
    if err is not None:
        QMessageBox.critical(self.window, "Error", f"{str(err)}")
        return 
    else: 
        self.DTData.accuracy = accuracy
        self.DTData.f1score = f1score
        self.DTData.classifier = classifier
        self.DTData.gini = gini
        self.DTData.class_report = cls_report
        self.DTData.confusion_matrix = conf_matrix
        set_dt_info(self)
        self.saveModelButtonDT.show()
        self.viewTreeButton.show()
        self.viewCMButton.show()

def save_dt_model(self):

    classifier = self.DTData.classifier 
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

def load_dt_model(self):
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
            self.DTData.classifier = classifier
            QMessageBox.information(self.window, "Success", f"Model loaded from {file_path}")
            self.loadedModelLabelDT.setText(file_path)
            self.loadedModelLabelDT.show()
            QMessageBox.warning(self.window, "Important", "Be mindful that models must be used in a dataset with same features as the one it was trained on.")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to load model: {str(e)}")

def view_tree(self):
    tree = DecisionTreeDialog(self.DTData.classifier)
    tree.exec_()

def show_dataframe_sample(self):
    df_sample = self.current_dataframe.head()
    self.dialog = DataFrameDialog(df_sample)
    self.dialog.exec_()

def view_confusion_matrix(self):
    cmDialog = ConfusionMatrixDialog(self.DTData.confusion_matrix)
    cmDialog.exec_()

def apply_dt_over_dataset(self):
    try:
        if not hasattr(self.DTData, 'classifier') or self.DTData.classifier is None:
            raise ValueError("Classifier is not initialized.")
        if not hasattr(self, 'current_dataframe') or self.current_dataframe is None:
            raise ValueError("Current dataframe is not initialized.")
        
        classifier = self.DTData.classifier
        df = self.current_dataframe.copy()
        
        expected_features = classifier.feature_names_in_
        if not all(feature in df.columns for feature in expected_features):
            raise ValueError("Current dataframe does not contain the expected features.")
        
        predictions = classifier.predict(df[expected_features])
        df['Pred'] = predictions
        self.current_dataframe = df
        
        self.predictedDFInfo = QTableWidget(parent=self.dtInfoData.parent())
        self.predictedDFInfo.setGeometry(self.dtInfoData.geometry())
        self.predictedDFInfo.setStyleSheet("border: 1px solid black;")

        self.savePredictedDFButtonDT = QPushButton(parent = self.dtInfoData.parent())
        self.savePredictedDFButtonDT.setGeometry(self.saveModelButtonDT.geometry())
        self.savePredictedDFButtonDT.clicked.connect(lambda: save_data(self, self.current_dataframe))
        self.savePredictedDFButtonDT.setText("Save DF")
        self.savePredictedDFButtonDT.show()
        
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


class DT_Data:
    def __init__(self, accuracy=None, f1score=None, classifier=None, classification_report=None, confusion_matrix = None,gini=None):
        self.accuracy = accuracy
        self.f1score = f1score
        self.classifier = classifier 
        self.class_report = classification_report
        self.gini = gini
        self.confusion_matrix = confusion_matrix
