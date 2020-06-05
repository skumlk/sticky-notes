from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFrame, QMenu, QMessageBox

import app.shared.util as util
from PyQt5.Qt import QColor
from PyQt5.QtGui import QTextCursor
from app.bin.Settings import Settings

class StickyNoteEditor(QtWidgets.QTextEdit):

    color_list = ["purple", "green", "pink", "yellow"]

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setSettings(settings)

        self._setStyleSheet()
        boldAction = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+B"), self)
        boldAction.activated.connect(self.boldAction)

        italicAction = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+I"), self)
        italicAction.activated.connect(self.italicAction)

        strikeThroughAction = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        strikeThroughAction.activated.connect(self.strikeThroughAction)

        unerlineAction = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+U"), self)
        unerlineAction.activated.connect(self.underlineAction)

        self.cursorPositionChanged.connect(self.cursorPositionChangedAction)

        redColor = QColor(255, 0, 0)
        blackColor = QColor(0, 0, 0)

        #self.setTextColor(QColor(255,0,0))

        currentFormat = self.currentCharFormat()
        currentFormat.setForeground(QColor(255,0 ,0))
        self.setCurrentCharFormat(currentFormat)

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
        if currentFormat.fontWeight() == 75:
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

    def _setStyleSheet(self):

        self.setStyleSheet("""
            QScrollBar:vertical {
                background: #F1F1F1;
                width:15px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background:#C0C0C0;
                width:15px;
                margin: 1px;
            }
            QScrollBar::handle:vertical:hover {
                background:#A8A8A8;
            }
            QScrollBar::add-line:vertical {
                background: #CE00CE;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: #CE00CE;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)

    def setColor(self, color : QColor):
        currentFormat = self.currentCharFormat()
        currentFormat.setForeground(color)
        self.setCurrentCharFormat(currentFormat)

    def setFontSize(self, fontSize):
        currentFormat = self.currentCharFormat()
        currentFormat.setFontPointSize(fontSize)
        self.setCurrentCharFormat(currentFormat)

    def setFontFamily(self, fontFamily):
        currentFormat = self.currentCharFormat()
        currentFormat.setFontFamily(fontFamily)
        self.setCurrentCharFormat(currentFormat)

    def setText(self, text):
        super().setText(text)

    def setSettings(self, settings: Settings):
        self.settings = settings

    def updateSettingsCursor(self):
        currentFormat = self.currentCharFormat()
        currentFormat.setForeground(self.settings.getFontColor())
        currentFormat.setFontFamily(self.settings.getFontFamily())
        currentFormat.setFontPointSize(self.settings.getFontSize())
        self.setCurrentCharFormat(currentFormat)

    def cursorPositionChangedAction(self):
        self.updateSettingsCursor()