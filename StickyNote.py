import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame, QMenu, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from Titlebar import TitleBar
import Const

class StickyNoteEditor(QtWidgets.QTextEdit):

    color_list = ["purple", "green", "pink", "yellow"]

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

    def isSelected(self):
        cursor = self.textCursor()
        return cursor.selectionEnd() - cursor.selectionStart()

    def contextMenuEvent(self, event):

        contextMenu = QMenu(self)
        isSelected = self.isSelected()

        copyAction = contextMenu.addAction("Copy")
        copyAction.triggered.connect(self.copy_action)

        cutAction = contextMenu.addAction("Cut")
        cutAction.triggered.connect(self.cut_action)

        pasteAction = contextMenu.addAction("Paste")
        pasteAction.triggered.connect(self.paste_action)

        deleteAction = contextMenu.addAction("Delete")
        deleteAction.triggered.connect(self.delete_action)

        selectAllAction = contextMenu.addAction("Select All")
        selectAllAction.triggered.connect(self.select_all_action)

        if(not isSelected):
            copyAction.setEnabled(False)
            cutAction.setEnabled(False)
            deleteAction.setEnabled(False)

        if not self.canPaste():
            pasteAction.setEnabled(False)
       
        contextMenu.addSeparator()

        for color in self.color_list:
            contextMenu.addAction(QtGui.QIcon('img/{0}.png'.format(color)), color.title())

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action:
            color =  action.text().lower()
            if color in self.color_list:
                self.parent.setColor(color)

    def copy_action(self):
        self.copy()

    def paste_action(self):
        self.paste()

    def delete_action(self):
        pass

    def select_all_action(self):
        self.selectAll()

    def cut_action(self):
        self.cut()

class StickyNote(QtWidgets.QFrame):

    bodyColors = {"purple": "#D700D7", "green": "#D4FC7A","yellow": "#FFE46E","pink": "#FF7BE3" }
    titleColors = {"purple": "#AA00AA", "green": "#BFFB33","yellow": "#FFDB3B","pink": "#FF48D8" }

    def __init__(self, _id, noteManager, parent=None):
        
        QtWidgets.QFrame.__init__(self, parent)
        
        self._id = _id
        self.noteManager = noteManager
        self.m_mouse_down= False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
       
        self.updateStyleSheet()
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
        self.textEditor=StickyNoteEditor(self)
        self.textEditor.setFrameStyle(QFrame.NoFrame)
        l.addWidget(self.textEditor)
        self.textEditor.textChanged.connect(self.signalTextChanged)

    def contentWidget(self):
        return self.m_content

    def setText(self, text):
        self.textEditor.setText(text)

    def setPosition(self, x, y):
        self.move(x, y)

    def signalTextChanged(self):
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
        msg = QMessageBox()
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

    def updateStyleSheet(self, backgroundColor = Const.BODY_BACKGROUND_COLOR):
        css = """
            QFrame{{
                Background:  {0};
                color:white;
                font:13px ;
                font-weight:bold;
                }}
            """.format(backgroundColor)
        self.setStyleSheet(css)

    def setColor(self, color):
        bodyColorCode = self.bodyColors[color]
        titleColorCode = self.titleColors[color]
        self.updateStyleSheet(bodyColorCode)
        self.noteManager.updateNoteColor(self._id, color)
        self.m_titleBar.updateTitleColor(titleColorCode)