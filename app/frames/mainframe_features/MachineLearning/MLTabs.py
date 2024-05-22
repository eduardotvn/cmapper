from PyQt5 import QtCore, QtGui, QtWidgets
from .DecisionTree.loadDTButtons import load_dt_buttons

def load_machine_learning_tabs(self, parent):
    self.running_feature.hide()

    if self.current_dataframe is None:
        self.set_dataframe()

    self.MLGB = QtWidgets.QGroupBox(parent)
    self.MLGB.setGeometry(QtCore.QRect(210, 30, 811, 521))
    self.MLGB.setTitle("")

    self.MLGBTabs = QtWidgets.QTabWidget(self.MLGB)
    self.MLGBTabs.setGeometry(QtCore.QRect(0, 30, 811, 521))

    self.tab_decision_tree = QtWidgets.QWidget()
    self.tab_linear_regression = QtWidgets.QWidget()
    self.tab_svm = QtWidgets.QWidget()
    self.tab_logistic_regression = QtWidgets.QWidget()
    self.tab_knn = QtWidgets.QWidget()

    self.MLGBTabs.addTab(self.tab_decision_tree, "Decision Tree")
    self.MLGBTabs.addTab(self.tab_linear_regression, "Linear Regression")
    self.MLGBTabs.addTab(self.tab_svm, "SVM")
    self.MLGBTabs.addTab(self.tab_logistic_regression, "Logistic Regression")
    self.MLGBTabs.addTab(self.tab_knn, "KNN")

    load_dt_buttons(self, self.tab_decision_tree)

    self.running_feature = self.MLGB
    self.running_feature.show()
