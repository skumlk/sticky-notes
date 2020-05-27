
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFontComboBox, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.Qt import QColorDialog, Qt

class SettingsDialog(QDialog):

    def __init__(self, color = None, fontSize = None, fontFamily = None):
        super(SettingsDialog, self).__init__()
        self.setWindowTitle("Sticky Note - Settings")
        self.layout = QFormLayout()
      
        self.fontSizeBox = QComboBox(self)
        for i in [8, 10, 12 ,14,16,18,22,24]:
            self.fontSizeBox.addItem(str(i))
        self.layout.addRow("Font size", self.fontSizeBox)

        self.fontFamilyBox = QFontComboBox(self)
        self.layout.addRow("Font Family", self.fontFamilyBox)

        self.colorButton = QPushButton('', self)
        color = QColor(Qt.blue)
        self.updateColor(color)
        self.colorButton.clicked.connect(self.showColors)
        self.layout.addRow("Font Color", self.colorButton)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)

        self.setLayout(self.layout)
        #self.resize(100, 100)
        self.setWindowFlags(Qt.Window)
        self.setFixedSize(350, 150)


    def updateColor(self, color):
        if(color.isValid()):
            self.colorButton.setStyleSheet("background-color: {0};border-color: {0}".format(color.name()))

    def showColors(self):
        colorDialog = QColorDialog()
        color = colorDialog.getColor()
        if color:
            self.updateColor(color)