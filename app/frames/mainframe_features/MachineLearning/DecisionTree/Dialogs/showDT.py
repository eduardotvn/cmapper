import sys
import graphviz
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from sklearn.tree import export_graphviz

class DecisionTreeDialog(QDialog):
    def __init__(self, classifier):
        super().__init__()
        self.classifier = classifier
        self.setWindowTitle("Decision Tree Visualization")
        self.setGeometry(100, 100, 600, 450)
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.visualize_decision_tree()

    def visualize_decision_tree(self):
        dot_data = export_graphviz(
            self.classifier,
            out_file=None,
            feature_names=None,
            class_names=None,
            filled=True,
            rounded=True,
            special_characters=True
        )
        graph = graphviz.Source(dot_data)
        graph.render("decision_tree", format='png', cleanup=True)
        image_path = "decision_tree.png"
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)
