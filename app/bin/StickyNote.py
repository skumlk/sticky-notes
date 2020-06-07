import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame, QMenu, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from app.bin.Titlebar import TitleBar
import app.bin.Const
from app.bin.StickyNoteEditor import StickyNoteEditor
from PyQt5.Qt import QColor, pyqtSignal
from app.bin import ConfigParser
from app.bin.Settings import Settings
from app.bin.ConfigParser import ConfigNoteModel

class StickyNote(QtWidgets.QFrame):

    #pin to top, undo not working properly
    reopenWindowSignal = pyqtSignal(str)

    bodyColors = {"purple": "#eb00eb", "green": "#D4FC7A","yellow": "#FFE46E","pink": "#FF7BE3" }
    titleColors = {"purple": "#D700D7", "green": "#BFFB33","yellow": "#FFDB3B","pink": "#FF48D8" }

    def __init__(self, _id, noteManager, configNote: ConfigNoteModel, parent=None):
        
        QtWidgets.QFrame.__init__(self, parent)
        
        self._id = _id
        self.noteManager = noteManager
        self.m_mouse_down= False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
       
        self.updateStyleSheet()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        settings = ConfigParser.config_instance.getSettings()
        self.m_titleBar = TitleBar(self, configNote.isPinToTop())
        self.m_content = QtWidgets.QWidget(self)
        vbox=QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        layout=QtWidgets.QVBoxLayout()
        layout.addWidget(self.m_content)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        vbox.addLayout(layout)

        l=QtWidgets.QVBoxLayout(self.contentWidget())
        l.setContentsMargins(0, 0, 0, 0)
        settings = ConfigParser.config_instance.getSettings()
        self.textEditor=StickyNoteEditor(settings, self)
        self.textEditor.setFrameStyle(QFrame.NoFrame)
        l.addWidget(self.textEditor)
        self.textEditor.textChanged.connect(self.signalTextChanged)
        self.m_titleBar.pinToTopChangeSignal.connect(self.actionPinToTopChange)

        self.setText(configNote.getText())
        self.setPosition(configNote.getX(), configNote.getY())
        self.setDimension(configNote.getWidth(), configNote.getHeight())
        self.setPinToTop(configNote.isPinToTop())

    def setPinToTop(self, isPinToTop):
        flag = self.windowFlags()
        if isPinToTop:
            flag |= Qt.WindowStaysOnTopHint
            self.setWindowFlags(flag)
            self.raise_()
            self.show()
            self.activateWindow()
        elif bool(flag & QtCore.Qt.WindowStaysOnTopHint):#is flag set
            self.close()
            self.reopenWindowSignal.emit(self._id)

    def actionPinToTopChange(self, isPinToTop):
        ConfigParser.config_instance.updateNotePinToTop(self._id, isPinToTop)
        self.setPinToTop(isPinToTop)

    def contentWidget(self):
        return self.m_content

    def setText(self, text):
        self.textEditor.setText(text)

    def setPosition(self, x, y):
        self.move(x, y)

    def signalTextChanged(self):
        text = self.textEditor.toHtml()
        self.noteManager.updateNoteText(self._id, text)

    def positionChanged(self, x,y):
        self.noteManager.updateNotePosition(self._id, x, y)

    def resizeEvent(self, resizeEvent):
        newSize = self.size()
        self.noteManager.updateNoteDimension(self._id, newSize.width(), newSize.height())

    def setDimension(self, width, height):
        self.resize(width, height)

    def closeNote(self):
        msg = QMessageBox()
        msg.move(self.geometry().x(), self.geometry().y() + 50)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Do you want to delete note?")
        msg.setWindowTitle("Sticky Note")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        if retval == QMessageBox.Ok:  # accepted
            self.close()
            self.noteManager.deleteNote(self._id)

    def createNewNote(self):
        self.noteManager.createNewNote(self._id)

    def updateStyleSheet(self, backgroundColor = app.bin.Const.BODY_BACKGROUND_COLOR):
        css = """
            QFrame{{
                Background:  {0};
                color: black;
                font:13px ;
                font-weight:normal;
                }}
            """.format(backgroundColor)
        self.setStyleSheet(css)

    def setColor(self, color):
        bodyColorCode = self.bodyColors[color]
        titleColorCode = self.titleColors[color]
        self.updateStyleSheet(bodyColorCode)
        self.noteManager.updateNoteColor(self._id, color)
        self.m_titleBar.updateTitleColor(titleColorCode)

    def updateSettings(self):
        settings = ConfigParser.config_instance.getSettings()
        self.textEditor.setSettings(settings)

        # self.textEditor.setColor(settings.getFontColor())
        # self.textEditor.setFontSize(settings.getFontSize())
        # self.textEditor.setFontFamily(settings.getFontFamily())