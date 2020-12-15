
import os
import sys
from PyQt5 import QtWidgets, QtGui

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bin.ConfigParser as ConfigParser
from bin.SystemTray import SystemTrayIcon
from bin.MemoryCondition import MemoryCondition
import bin.StickyNoteManager as StickyNoteManager
import shared.util as util

# import qtmodern.styles
# import qtmodern.windows
import os
# from qtpy import QtCore
from PyQt5.Qt import QMainWindow
from PyQt5.QtCore import Qt

def _app():
    iconPath = 'img/stickynotes.png'
    app = QtWidgets.QApplication(sys.argv)
    # qtmodern.styles.dark(app)
    app.setQuitOnLastWindowClosed(False)

    w = QtWidgets.QWidget()
    app.setWindowIcon(util.createQIcon(__name__, iconPath))
    trayIcon = SystemTrayIcon(util.createQIcon(__name__, iconPath), w)
    trayIcon.show()
    ConfigParser.config_instance = ConfigParser.Config()
    StickyNoteManager.sticky_note_manager_instance = StickyNoteManager.StickyNoteManager()
    sys.exit(app.exec_())

def main():
    with MemoryCondition(key="skstickynote") as condition:
        if condition:
            _app()
        else:
            sys.exit(0)


if __name__ == '__main__':
    main()