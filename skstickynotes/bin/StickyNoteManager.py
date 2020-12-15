
from bin.StickyNote import StickyNote
from PyQt5 import QtWidgets, QtCore, QtGui
import bin.ConfigParser as ConfigParser
from PyQt5.Qt import QColor

class StickyNoteManager:

    stickyNotes = []

    def __init__(self):
        rec = QtWidgets.QApplication.desktop().screenGeometry()
        self.screenWidth = rec.width()

        for note in ConfigParser.config_instance.getNotes(): 
           self.createNote(note)

    def createNote(self, note: ConfigParser.ConfigNoteModel):
        _id = note.getId()
        stickyNote = StickyNote(_id, self, note)
        stickyNote.updateSettings()
        stickyNote.show()
        stickyNote.setColor(note.getColor())
        self.stickyNotes.append(stickyNote)
        stickyNote.reopenWindowSignal.connect(self.actionReopenStickyNote)
        return stickyNote

    def createNewNote(self, _id = None):

        x = self.screenWidth - 300
        y = 250
        color = "purple"

        if _id:
            note = ConfigParser.config_instance.getNote(_id)
            x = note.getX()
            y = note.getY() + 100
            color = note.getColor()

        note = ConfigParser.config_instance.createNewNote(x, y, color)
        self.createNote(note)

    def showAll(self):
        for frame in self.stickyNotes:
            frame.show()
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

    def hideAll(self):
        for frame in self.stickyNotes:
            frame.hide()     

    def updateSettings(self):
        for stickyNote in self.stickyNotes:
            stickyNote.updateSettings()

    def actionReopenStickyNote(self, _id):
        self.stickyNotes = [x for x in self.stickyNotes if x._id != _id]
        note = ConfigParser.config_instance.getNote(_id)
        self.createNote(note)

sticky_note_manager_instance = None