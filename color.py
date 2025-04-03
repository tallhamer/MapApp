from PySide6.QtWidgets import QApplication, QPushButton, QColorDialog, QVBoxLayout, QWidget
from PySide6.QtGui import QColor
import sys

class ColorDialogExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QColorDialog Example")
        self.button = QPushButton("Open Color Dialog", self)
        self.button.clicked.connect(self.showColorDialog)
        self.color = QColor(255, 255, 255)  # Default color

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def showColorDialog(self):
        self.color = QColorDialog.getColor(self.color, self, "Select Color")
        if self.color.isValid():
            print(f"Selected color: {self.color.getRgb()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = ColorDialogExample()
    example.show()
    sys.exit(app.exec())