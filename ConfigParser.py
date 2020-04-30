
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

    def addNote(self, text, color, x, y, width, height):
        self.data["notes"].append({
            "id": uuid.uuid4(),
            "width": width,
            "height": height,
            "x": x,
            "y": y,
            "text": text,
            "color": color
        })
        self._updateNote()

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

    def updateNotePosition(self, id, x, y):
        note = self.getNote(id)
        if note:
            note["x"] = x
            note["y"] = y
            self._updateNote()

    def updateNoteDimension(self, id, width, height):
        note = self.getNote(id)
        if note:
            note["width"] = width
            note["height"] = height
            self._updateNote()

    def updateNoteColor(self, color):
        note = self.getNote(id)
        if note:
            note["color"] = color
            self._updateNote()

config_instance = None#should initialize by main