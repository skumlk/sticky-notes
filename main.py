
import os
import sys
from PyQt5 import QtWidgets, QtGui

sys.path.insert(1, './bin')
import ConfigParser
from SystemTray import SystemTrayIcon
import StickyNoteManager

import qtmodern.styles
import qtmodern.windows

def main(image):
    app = QtWidgets.QApplication(sys.argv)
    qtmodern.styles.dark(app)
    app.setQuitOnLastWindowClosed(False)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()

    config_file = "config/config.json"
    ConfigParser.config_instance = ConfigParser.Config(config_file)
    StickyNoteManager.sticky_note_manager_instance = StickyNoteManager.StickyNoteManager()

    sys.exit(app.exec_())

if __name__ == '__main__':
    icon = 'img/icon.png'
    main(icon)