

import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFrame
from bin.StickyNote import StickyNote
import bin.StickyNoteManager as StickyNoteManager
from bin.SettingsDialog import SettingsDialog
import bin.ConfigParser as ConfigParser
# import qtmodern.styles
# import qtmodern.windows
# import qtmodern

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        create_new_action = menu.addAction('New Note')
        hide_all_action = menu.addAction('Hide All')
        menu.addSeparator()
        settings_action = menu.addAction('Settings')
        menu.addSeparator()
        exit_action = menu.addAction('Quit')

        self.setContextMenu(menu)

        create_new_action.triggered.connect(self.createNote)
        exit_action.triggered.connect(self.exitAll)
        settings_action.triggered.connect(self.showSettings)
        hide_all_action.triggered.connect(self.hideAll)
        menu.aboutToShow.connect(self.action)


    def on_context_menu(self, point):
        pass

    def action(self):
        StickyNoteManager.sticky_note_manager_instance.showAll()   

    def createNote(self):
        StickyNoteManager.sticky_note_manager_instance.createNewNote()

    def hideAll(self):
        StickyNoteManager.sticky_note_manager_instance.hideAll()   

    def exitAll(self):
        QtWidgets.QApplication.quit()

    def showSettings(self):
        settings = ConfigParser.config_instance.getSettings()
        dlg = SettingsDialog(settings)
        dlg.move(self.geometry().x(), self.geometry().y() + 50)
        # mw = qtmodern.windows.ModernWindow(dlg)
        ret = dlg.show()
