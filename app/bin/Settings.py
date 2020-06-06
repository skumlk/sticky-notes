from PyQt5.QtGui import QColor

class Settings:

    FONT_SIZE = "fontSize"
    FONT_COLOR = "fontColor"
    FONT_NAME = "fontFamily"
    IS_PIN_TO_TOP = "isPinToTop"

    def __init__(self, jsonStruct):
        
        fontSize = 10
        fontFamily = "sans-serif"
        fontColor = "#ffffff"
        isPinToTop = False

        if jsonStruct:
            if self.FONT_SIZE in jsonStruct:
                fontSize = jsonStruct[self.FONT_SIZE]

            if self.FONT_COLOR in jsonStruct:
                fontColor = jsonStruct[self.FONT_COLOR]

            if self.FONT_SIZE in jsonStruct:
                fontFamily = jsonStruct[self.FONT_NAME]

            if self.IS_PIN_TO_TOP in jsonStruct:
                isPinToTop = jsonStruct[self.IS_PIN_TO_TOP] == 1

        self.setFontSize(fontSize)
        self.setFontColor(fontColor)
        self.setFontFamily(fontFamily)
        self.setPinToTop(isPinToTop)

    def getAllFontSizes(self):
        return [8, 10, 12 ,14,16,18,22,24]

    def getFontSize(self):
        return self.fontSize

    def getFontFamily(self):
        return self.fontFamily
    
    def getFontColor(self):
        return QColor(self.fontColor)

    def getPinToTop(self):
        return self.isPinToTop

    def setFontSize(self, fontSize):
        try:
            self.fontSize = int(fontSize)
        except:
            return

    def setFontFamily(self, fontFamily):
        self.fontFamily = fontFamily
    
    def setFontColor(self, fontColor):
        self.fontColor = fontColor

    def setPinToTop(self, isPinToTop):
        self.isPinToTop = int(isPinToTop)

    def getJSON(self):
        isPinToTop = 0
        if self.isPinToTop:
            isPinToTop = 1
        return {
            self.FONT_SIZE : self.fontSize,
            self.FONT_COLOR : self.fontColor,
            self.FONT_NAME : self.fontFamily,
            self.IS_PIN_TO_TOP : isPinToTop,
        }
