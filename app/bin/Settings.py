from PyQt5.QtGui import QColor

class Settings:

    FONT_SIZE = "fontSize"
    FONT_COLOR = "fontColor"
    FONT_NAME = "fontFamily"

    def __init__(self, jsonStruct):
        
        fontSize = 10
        fontFamily = "sans-serif"
        fontColor = "#ffffff"

        if jsonStruct:
            if self.FONT_SIZE in jsonStruct:
                fontSize = jsonStruct[self.FONT_SIZE]

            if self.FONT_COLOR in jsonStruct:
                fontColor = jsonStruct[self.FONT_COLOR]

            if self.FONT_SIZE in jsonStruct:
                fontFamily = jsonStruct[self.FONT_NAME]

        self.setFontSize(fontSize)
        self.setFontColor(fontColor)
        self.setFontFamily(fontFamily)

    def getAllFontSizes(self):
        return [8, 10, 12 ,14,16,18,22,24]

    def getFontSize(self):
        return self.fontSize

    def getFontFamily(self):
        return self.fontFamily
    
    def getFontColor(self):
        return QColor(self.fontColor)

    def setFontSize(self, fontSize):
        try:
            self.fontSize = int(fontSize)
        except:
            return

    def setFontFamily(self, fontFamily):
        self.fontFamily = fontFamily
    
    def setFontColor(self, fontColor):
        self.fontColor = fontColor

    def getJSON(self):
        return {
            self.FONT_SIZE : self.fontSize,
            self.FONT_COLOR : self.fontColor,
            self.FONT_NAME : self.fontFamily,
        }
