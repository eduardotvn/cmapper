import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import colors

class CorrelationMatrixDialog(QtWidgets.QDialog):
    def __init__(self, df_corr, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Correlation Matrix")
        self.setGeometry(100, 100, 800, 600)
        
        self.canvas = FigureCanvas(plt.Figure())
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        self.plot_correlation_matrix(df_corr)
        
    def plot_correlation_matrix(self, df_corr):
        cmap = colors.ListedColormap(["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60"])
        ax = self.canvas.figure.add_subplot(111)  
        sns.heatmap(df_corr, annot=True, cmap=cmap, center=0, ax=ax, fmt=".2f", annot_kws={"size": 8})
        ax.tick_params(axis='x', rotation=45)  
        ax.tick_params(axis='y', rotation=0)  
        plt.tight_layout()  
        self.canvas.draw()


