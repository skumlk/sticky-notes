
import os
import sys
from PyQt5 import QtWidgets, QtGui
import ConfigParser
from SystemTray import SystemTrayIcon
import StickyNoteManager

def main(image):
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()

    config_file = "config.json"
    ConfigParser.config_instance = ConfigParser.Config(config_file)
    StickyNoteManager.sticky_note_manager_instance = StickyNoteManager.StickyNoteManager()

    sys.exit(app.exec_())

if __name__ == '__main__':
    icon = 'img/icon.png'
    main(icon)