import os
import json
import uuid
import appdirs
import errno

from bin.Settings import Settings

AppName = "StickyNotes"
AuthorName = "Samlk"
CONFIG_FILE_NAME = "config.json"

INIT_CONFIG_DATA = {"notes": [],  "settings": {}}

NOTE_IS_PIN_TO_TOP = "isPinToTop"
NOTE_WIDTH = "width"
NOTE_HEIGHT = "height"
NOTE_TEXT = "text"
NOTE_X = "x"
NOTE_Y = "y"
NOTE_COLOR = "color"
NOTE_ID = "id"

class ConfigNoteModel:

    isPinToTopDefault = False

    def __init__(self, jsonStruct):
        self.jsonStruct = jsonStruct

    def isPinToTop(self):
        if NOTE_IS_PIN_TO_TOP in self.jsonStruct:
            return self.jsonStruct[NOTE_IS_PIN_TO_TOP] == 1

        return self.isPinToTopDefault

    def getWidth(self):
        return self.jsonStruct[NOTE_WIDTH]

    def getHeight(self):
        return self.jsonStruct[NOTE_HEIGHT]

    def getText(self):
        return self.jsonStruct[NOTE_TEXT]

    def getX(self):
        return self.jsonStruct[NOTE_X]

    def getY(self):
        return self.jsonStruct[NOTE_Y]

    def getColor(self):
        return self.jsonStruct[NOTE_COLOR]

    def getId(self):
        return self.jsonStruct[NOTE_ID]

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
            self._writeToConfig(INIT_CONFIG_DATA, True)

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
            return [ConfigNoteModel(x) for x in notes]

        return []

    def createNewNote(self, x, y, color = "purple", width = 300, height = 250, text = ""):
        note = {
            NOTE_ID: str(uuid.uuid4()),
            NOTE_WIDTH: width,
            NOTE_HEIGHT: height,
            NOTE_X: x,
            NOTE_Y: y,
            NOTE_TEXT: text,
            NOTE_COLOR: color,
            NOTE_IS_PIN_TO_TOP: 0
        }
        self.data["notes"].append(note)
        self._updateNote()
        return ConfigNoteModel(note)

    def getNote(self, id):
        note = self._getNote(id)
        if note:
            return ConfigNoteModel(note)

        return None

    def _getNote(self, id):
        e1 = [note for note in self.data["notes"] if note["id"] == id]
        if e1 and len(e1) > 0:
            return e1[0]

        return None

    def updateNoteText(self, id, text):
        note = self._getNote(id)
        if note:
            note["text"] = text
            self._updateNote()

    def updateNotePosition(self, _id, x, y):
        note = self._getNote(_id)
        if note:
            note["x"] = x
            note["y"] = y
            self._updateNote()

    def updateNoteDimension(self, _id, width, height):
        note = self._getNote(_id)
        if note:
            note["width"] = width
            note["height"] = height
            self._updateNote()

    def updateNoteColor(self, _id, color):
        note = self._getNote(_id)
        if note:
            note["color"] = color
            self._updateNote()

    def updateNotePinToTop(self, _id, isPinToTop):
        note = self._getNote(_id)
        if note:
            pinToTop = 0
            if isPinToTop:
                pinToTop = 1
            note[NOTE_IS_PIN_TO_TOP] = pinToTop
            self._updateNote()

    def deleteNote(self, _id):
        notes = [note for note in self.data["notes"] if note["id"] != _id]
        self.data["notes"] = notes
        self._updateNote()

    def saveSettings(self, settings: Settings):
        self.data["settings"] = settings.getJSON()
        self._updateNote()

    def getSettings(self):
        settings = None
        if("settings" in self.data):
            settings = self.data["settings"]

        return Settings(settings)
    
config_instance = None#should initialize by main