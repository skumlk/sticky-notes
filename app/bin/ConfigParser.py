import os
import json
import uuid
import appdirs
import errno

AppName = "StickyNotes"
AuthorName = "Samlk"
CONFIG_FILE_NAME = "config.json"

class Config:
    
    def __init__(self) :
        location = appdirs.user_data_dir(AppName, AuthorName)
        self.configFileName = os.path.join(location, CONFIG_FILE_NAME)
        if not os.path.exists(location):
            try:
                os.makedirs(location)
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        if not os.path.isfile(self.configFileName):
            data = {"notes": []}
            self._writeToConfig(data, True)

        with open(self.configFileName, 'r') as json_file:
            self.data = json.load(json_file)

    def _writeToConfig(self, data, isCeateIfNotExist = False):
        flag = "w"
        if isCeateIfNotExist:
            flag = "w+"
        with open(self.configFileName, flag) as f:
            json.dump(data, f)

    def _updateNote(self):
        self._writeToConfig(self.data)

    def getNotes(self):
        notes = self.data["notes"]
        if notes:
            return notes

        return []

    def createNewNote(self, x, y, color = "purple", width = 300, height = 250, text = ""):
        note = {
            "id": str(uuid.uuid4()),
            "width": width,
            "height": height,
            "x": x,
            "y": y,
            "text": text,
            "color": color
        }
        self.data["notes"].append(note)
        self._updateNote()
        return note

    def getNote(self, id):
        e1 = [note for note in self.data["notes"] if note["id"] == id]
        if e1 and len(e1) > 0:
            return e1[0]

        return None

    def updateNoteText(self, id, text):
        note = self.getNote(id)
        if note:
            note["text"] = text
            self._updateNote()

    def updateNotePosition(self, _id, x, y):
        note = self.getNote(_id)
        if note:
            note["x"] = x
            note["y"] = y
            self._updateNote()

    def updateNoteDimension(self, _id, width, height):
        note = self.getNote(_id)
        if note:
            note["width"] = width
            note["height"] = height
            self._updateNote()

    def updateNoteColor(self, _id, color):
        note = self.getNote(_id)
        if note:
            note["color"] = color
            self._updateNote()

    def deleteNote(self, _id):
        notes = [note for note in self.data["notes"] if note["id"] != _id]
        self.data["notes"] = notes
        self._updateNote()

config_instance = None#should initialize by main