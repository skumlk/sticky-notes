import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class TitleBar(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        css = """
        QWidget{
            Background: #AA00AA;
            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            font-size:12px;
            color: black;
        }
        QToolButton{
            Background:#AA00AA;
            font-size:11px;
        }
        QToolButton:hover{
        }
        """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)
        hbox=QtWidgets.QHBoxLayout(self)

        btnClose=QtWidgets.QToolButton(self)
        btnClose.setIcon(QtGui.QIcon('img/close.png'))
        btnClose.setMinimumHeight(10)
        btnClose.clicked.connect(self.close)
        hbox.addWidget(btnClose)

        btnCreateNewNote=QtWidgets.QToolButton(self)
        btnCreateNewNote.setIcon(QtGui.QIcon('img/new.png'))
        btnCreateNewNote.setMinimumHeight(10)
        btnCreateNewNote.clicked.connect(self.createNewNote)
        hbox.addWidget(btnCreateNewNote)
        

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