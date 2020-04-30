

import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFrame
from StickyNote import StickyNote
import StickyNoteManager

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        create_new_action = menu.addAction('Create New')
        exit_action = menu.addAction('Exit')

        self.setContextMenu(menu)
        create_new_action.triggered.connect(self.createNote)
        exit_action.triggered.connect(self.exitAll)
        menu.aboutToShow.connect(self.action)

    def action(self):
        StickyNoteManager.sticky_note_manager_instance.showAll()   

    def createNote(self):
        StickyNoteManager.sticky_note_manager_instance.createNote()

    def exitAll(self):
        QtWidgets.QApplication.quit()
