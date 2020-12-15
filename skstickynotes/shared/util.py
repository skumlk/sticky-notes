
import pkg_resources
from PyQt5.QtGui import QPixmap, QIcon

def createQIcon(mainName, fileName):
    image = pkg_resources.resource_string(mainName, fileName)
    qmap = QPixmap()
    qmap.loadFromData(image)
    return QIcon(qmap)

