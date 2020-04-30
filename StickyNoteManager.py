
from StickyNote import StickyNote
from PyQt5 import QtWidgets, QtCore, QtGui
import ConfigParser

class StickyNoteManager:

    stickyNotes = []

    def __init__(self):
        rec = QtWidgets.QApplication.desktop().screenGeometry()
        self.screenWidth = rec.width()

        for note in ConfigParser.config_instance.getNotes(): 
           self.createNote(note)

    def createNote(self, note):
        _id = note["id"]
        width = note["width"]
        height = note["height"]
        stickyNote = StickyNote(_id, self)
        stickyNote.setText(note["text"])
        stickyNote.setPosition(note["x"], note["y"])
        stickyNote.setDimension(width, height)
        stickyNote.show()
        stickyNote.setColor(note["color"])
        self.stickyNotes.append(stickyNote)
        return stickyNote

    def createNewNote(self, _id = None):

        x = self.screenWidth - 300
        y = 250
        color = "purple"

        if _id:
            note = ConfigParser.config_instance.getNote(_id)
            x = note["x"]
            y = note["y"] + 100
            color = note["color"]

        note = ConfigParser.config_instance.createNewNote(x, y, color)
        self.createNote(note)

    def showAll(self):
        for frame in self.stickyNotes:
            frame.activateWindow()     

    def updateNoteText(self, _id, text):
        ConfigParser.config_instance.updateNoteText(_id, text)

    def updateNotePosition(self, _id, x ,y):
        ConfigParser.config_instance.updateNotePosition(_id, x, y)

    def updateNoteDimension(self, _id,  width, height):
        ConfigParser.config_instance.updateNoteDimension(_id, width, height)

    def updateNoteColor(self, _id, color):
        ConfigParser.config_instance.updateNoteColor(_id, color)

    def deleteNote(self, _id):
        self.stickyNotes = [x for x in self.stickyNotes if x._id != _id]
        ConfigParser.config_instance.deleteNote(_id)        

sticky_note_manager_instance = None