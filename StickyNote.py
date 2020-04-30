import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from Titlebar import TitleBar

class StickyNote(QtWidgets.QFrame):
    def __init__(self, _id, noteManager, parent=None):
        
        QtWidgets.QFrame.__init__(self, parent)
        
        self._id = _id
        self.noteManager = noteManager
        self.m_mouse_down= False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        css = """
        QFrame{
            Background:  #D700D7;
            color:white;
            font:13px ;
            font-weight:bold;
            }
        """
        self.setStyleSheet(css)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar= TitleBar(self)
        self.m_content= QtWidgets.QWidget(self)
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
        self.textEditor=QtWidgets.QTextEdit()
        self.textEditor.setFrameStyle(QFrame.NoFrame)
        l.addWidget(self.textEditor)

        self.textEditor.textChanged.connect(self.textChanged)

    def contentWidget(self):
        return self.m_content

    def setText(self, text):
        self.textEditor.setText(text)

    def setPosition(self, x, y):
        self.move(x, y)

    def textChanged(self):
        text = self.textEditor.toPlainText()
        self.noteManager.updateNoteText(self._id, text)

    def positionChanged(self, x,y):
        self.noteManager.updateNotePosition(self._id, x, y)

    def resizeEvent(self, resizeEvent):
        newSize = self.size()
        self.noteManager.updateNoteDimension(self._id, newSize.width(), newSize.height())

    def setDimension(self, width, height):
        self.resize(width, height)

    def closeNote(self):
        self.close()
        self.noteManager.deleteNote(self._id)

    def createNewNote(self):
        self.noteManager.createNewNote()