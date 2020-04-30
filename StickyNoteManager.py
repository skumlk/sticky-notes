
from StickyNote import StickyNote
from PyQt5 import QtWidgets, QtCore, QtGui
import ConfigParser

class StickyNoteManager:

    stickyNotes = []

    def __init__(self):
        rec = QtWidgets.QApplication.desktop().screenGeometry()
        self.screenWidth = rec.width()

        for note in ConfigParser.config_instance.getNotes(): 
            _id = note["id"]
            width = note["width"]
            height = note["height"]
            stickyNote = self.createNote(_id)
            stickyNote.setText(note["text"])
            stickyNote.setPosition(note["x"], note["y"])
            stickyNote.setDimension(width, height)

    def createNote(self, _id):
        stickyNote = StickyNote(_id, self)
        stickyNote.move(self.screenWidth - 300, 60*len(self.stickyNotes))
        stickyNote.show()
        self.stickyNotes.append(stickyNote)
        return stickyNote

    def showAll(self):
        for frame in self.stickyNotes:
            frame.activateWindow()     

    def updateNoteText(self, _id, text):
        ConfigParser.config_instance.updateNoteText(_id, text)

    def updateNotePosition(self, _id, x ,y):
        ConfigParser.config_instance.updateNotePosition(_id, x, y)

    def updateNoteDimension(self, _id,  width, height):
        ConfigParser.config_instance.updateNoteDimension(_id, width, height)

sticky_note_manager_instance = None