import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import app.bin.Const
import app.shared.util as util
from PyQt5.Qt import pyqtSignal

class TitleBar(QtWidgets.QDialog):

    pinToTopChangeSignal = pyqtSignal(bool)

    def __init__(self, parent=None, isPinToToggle = False):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.updateCss()
        hbox=QtWidgets.QHBoxLayout(self)

        btnCreateNewNote=QtWidgets.QToolButton(self)
        btnCreateNewNote.setIcon(util.createQIcon("app", 'img/new.png'))
        btnCreateNewNote.setMinimumHeight(10)
        btnCreateNewNote.clicked.connect(self.createNewNote)
        hbox.addWidget(btnCreateNewNote)

        btnPinToggle=QtWidgets.QToolButton(self)
        self.btnPinToggle = btnPinToggle
        btnPinToggle.setMinimumHeight(10)
        btnPinToggle.clicked.connect(self.actionPinToggle)
        hbox.addWidget(btnPinToggle)
        self.setPinToToggle(isPinToToggle)
        
        btnClose=QtWidgets.QToolButton(self)
        btnClose.setIcon(util.createQIcon("app", 'img/close.png'))
        btnClose.setMinimumHeight(10)
        btnClose.clicked.connect(self.close)
        hbox.addWidget(btnClose)

        hbox.insertStretch(1,500)
        hbox.setSpacing(8)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.maxNormal=False

    def close(self):
        self.parent.closeNote()

    def createNewNote(self):
        self.parent.createNewNote()

    def setPinToToggle(self, isPinToToggle):
        self.isPinToToggle = isPinToToggle
        iconPath = 'img/pin-off.png'
        if self.isPinToToggle:
            iconPath = "img/pin-on.png"

        self.btnPinToggle.setIcon(util.createQIcon("app", iconPath))
        self.pinToTopChangeSignal.emit(self.isPinToToggle)

    def actionPinToggle(self):
        self.setPinToToggle(not self.isPinToToggle)

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.parent.moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.parent.moving: 
            newPosition = event.globalPos()-self.parent.offset
            self.parent.move(newPosition)
            self.parent.positionChanged(newPosition.x(), newPosition.y())
    
    def updateCss(self, backgroundColor=app.bin.Const.TITLE_BACKGROUND_COLOR):
        css = """
            QWidget{{
                Background: {0};
                color:white;
                font:12px bold;
                font-weight:bold;
                border-radius: 1px;
                height: 11px;
            }}
            QDialog{{
                font-size:12px;
                color: black;
            }}
            QToolButton{{
                Background: {0};
                font-size:11px;
            }}
            QToolButton:hover{{
            }}
        """.format(backgroundColor)
        self.setStyleSheet(css)


    def updateTitleColor(self, color):
        self.updateCss(color)