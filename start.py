
import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFrame
import stickyframe

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    stickyFrames = []

    def __init__(self, icon, app, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.app = app
        self.count = 0
        menu = QtWidgets.QMenu(parent)
        create_new_action = menu.addAction('Show All')
        create_new_action = menu.addAction('Create New')
        exit_action = menu.addAction('Exit')

        self.setContextMenu(menu)
        create_new_action.triggered.connect(self.createNew)
        exit_action.triggered.connect(self.exitAll)

        rec = QtWidgets.QApplication.desktop().screenGeometry()
        self.screenWidth = rec.width()
        menu.aboutToShow.connect(self.action)

    def action(self):
        for frame in self.stickyFrames:
            frame.activateWindow()

    def createNew(self):
        self.count += 1
        stickyFrame = stickyframe.StickyFrame()
        stickyFrame.move(self.screenWidth - 300, 60*self.count)
        l=QtWidgets.QVBoxLayout(stickyFrame.contentWidget())
        l.setContentsMargins(0, 0, 0, 0)
        textEditor=QtWidgets.QPlainTextEdit()
        textEditor.setFrameStyle(QFrame.NoFrame)
        l.addWidget(textEditor)
        stickyFrame.show()
        self.stickyFrames.append(stickyFrame)

    def exitAll(self):
        QtWidgets.QApplication.quit()

def main(image):
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), app, w)
    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    icon = 'img/icon.png'
    main(icon)