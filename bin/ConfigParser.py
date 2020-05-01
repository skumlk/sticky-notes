
import json
import uuid

class Config:
    
    def __init__(self, configFileName) :
        self.configFileName = configFileName
        with open(configFileName) as json_file:
            self.data = json.load(json_file)
    
    def _updateNote(self):
        with open(self.configFileName, 'w') as f:
            json.dump(self.data, f)

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