
import os
import sys
from PyQt5 import QtWidgets, QtGui

sys.path.insert(0, '/var/www/personal/sticky-notes')

import app.bin.ConfigParser as ConfigParser
from app.bin.SystemTray import SystemTrayIcon
import app.bin.StickyNoteManager as StickyNoteManager
import app.shared.util as util

import qtmodern.styles
import qtmodern.windows
import os

def main():

    iconPath = 'img/icon.png'
    app = QtWidgets.QApplication(sys.argv)
    qtmodern.styles.dark(app)
    app.setQuitOnLastWindowClosed(False)
    w = QtWidgets.QWidget()
    app.setWindowIcon(util.createQIcon(__name__, iconPath))
    trayIcon = SystemTrayIcon(util.createQIcon(__name__, iconPath), w)
    trayIcon.show()
    ConfigParser.config_instance = ConfigParser.Config()
    StickyNoteManager.sticky_note_manager_instance = StickyNoteManager.StickyNoteManager()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()