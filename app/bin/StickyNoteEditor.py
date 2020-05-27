from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFrame, QMenu, QMessageBox

import app.shared.util as util

class StickyNoteEditor(QtWidgets.QTextEdit):

    color_list = ["purple", "green", "pink", "yellow"]

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        boldAction = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+B"), self)
        boldAction.activated.connect(self.boldAction)

        italicAction = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+I"), self)
        italicAction.activated.connect(self.italicAction)

        strikeThroughAction = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        strikeThroughAction.activated.connect(self.strikeThroughAction)

        unerlineAction = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+U"), self)
        unerlineAction.activated.connect(self.underlineAction)

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
            contextMenu.addAction(util.createQIcon("app", 'img/{0}.png'.format(color)), color.title())

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

    def boldAction(self):
        currentFormat = self.currentCharFormat()
        if currentFormat.fontWeight == 75:
            newWeight = 50
        else:
            newWeight = 75

        currentFormat.setFontWeight(newWeight)
        self.setCurrentCharFormat(currentFormat)

    def italicAction(self):
        currentFormat = self.currentCharFormat()
        currentFormat.setFontItalic(not currentFormat.fontItalic())
        self.setCurrentCharFormat(currentFormat)

    def underlineAction(self):
        currentFormat = self.currentCharFormat()
        currentFormat.setFontUnderline(not currentFormat.fontUnderline())
        self.setCurrentCharFormat(currentFormat)

    def strikeThroughAction(self):
        currentFormat = self.currentCharFormat()
        currentFormat.setFontStrikeOut(not currentFormat.fontStrikeOut())
        self.setCurrentCharFormat(currentFormat)