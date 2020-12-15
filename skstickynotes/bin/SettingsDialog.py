
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFontComboBox, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QColor, QFont
from PyQt5.Qt import QCheckBox, QColorDialog, Qt
from bin.Settings import Settings
import bin.ConfigParser as ConfigParser
import bin.StickyNoteManager as  StickyNoteManager

class SettingsDialog(QDialog):

    def __init__(self, settings: Settings):
        super(SettingsDialog, self).__init__()
        self.settings = settings
        self.setWindowTitle("Sticky Note - Settings")
        self.layout = QFormLayout()
      
        self.fontSizeBox = QComboBox(self)
        for i in settings.getAllFontSizes():
            self.fontSizeBox.addItem(str(i))
        self.fontSizeBox.setCurrentText(str(settings.getFontSize()))
        self.layout.addRow("Font size", self.fontSizeBox)
        self.fontSizeBox.currentIndexChanged.connect(self.fontSizeChanged)

        self.fontFamilyBox = QFontComboBox(self)
        self.layout.addRow("Font Family", self.fontFamilyBox)
        self.fontFamilyBox.setCurrentFont(QFont(settings.getFontFamily()))
        self.fontFamilyBox.currentIndexChanged.connect(self.fontFamilyChanged)

        self.colorButton = QPushButton('', self)
        color = QColor(settings.getFontColor())
        self.fontColorChanged(color)
        self.colorButton.clicked.connect(self.showColors)
        self.layout.addRow("Font Color", self.colorButton)

        isAutoStartCheckBox = QCheckBox("Enable start on startup", self)
        #self.layout.addRow("", isAutoStartCheckBox)
        isAutoStartCheckBox.stateChanged.connect(self.actionEnableAutoStart)
        isAutoStartCheckBox.setChecked(settings.getStartOnStartup())

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)

        self.setLayout(self.layout)
        self.setWindowFlags(Qt.Window)
        self.setFixedSize(350, 150)

    def fontColorChanged(self, color):
        if(color.isValid()):
            self.colorButton.setStyleSheet("background-color: {0};border-color: {0}".format(color.name()))
            self.settings.setFontColor(color.name())

    def showColors(self):
        colorDialog = QColorDialog()
        color = colorDialog.getColor()
        if color:
            self.fontColorChanged(color)

    def fontSizeChanged(self):
        fontSize = str(self.fontSizeBox.currentText())
        self.settings.setFontSize(fontSize)

    def fontFamilyChanged(self):
        fontFamily = str(self.fontFamilyBox.currentText())
        self.settings.setFontFamily(fontFamily)

    def accept(self):
        ConfigParser.config_instance.saveSettings(self.settings)
        self.done(0)
        StickyNoteManager.sticky_note_manager_instance.updateSettings()        

    def reject(self):
        self.done(0)

    def actionEnableAutoStart(self, res):
        self.settings.setStartOnStartup(bool(res))
