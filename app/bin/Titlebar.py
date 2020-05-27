import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import app.bin.Const
import app.shared.util as util

class TitleBar(QtWidgets.QDialog):
    def __init__(self, parent=None):
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
        
        btnClose=QtWidgets.QToolButton(self)
        btnClose.setIcon(util.createQIcon("app", 'img/close.png'))
        btnClose.setMinimumHeight(10)
        btnClose.clicked.connect(self.close)
        hbox.addWidget(btnClose)

        hbox.insertStretch(1,500)
        hbox.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.maxNormal=False

    def close(self):
        self.parent.closeNote()

    def createNewNote(self):
        self.parent.createNewNote()

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