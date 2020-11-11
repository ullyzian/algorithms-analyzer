from PyQt5.QtCore import QObject, Qt, pyqtSignal


class Decorations(QObject):
    lineColorChanged = pyqtSignal(str)
    backgroundColorChanged = pyqtSignal(str)
    lineStyleChanged = pyqtSignal(object)
    lineWidthChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._lineColor = "#000000"
        self._backgroundColor = "#ffffff"
        self._lineStyle = Qt.SolidLine
        self._lineWidth = 3

    @property
    def lineColor(self):
        return self._lineColor

    @lineColor.setter
    def lineColor(self, value):
        self._lineColor = value
        self.lineColorChanged.emit(value)

    @property
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, value):
        self._backgroundColor = value
        self.backgroundColorChanged.emit(value)

    @property
    def lineStyle(self):
        return self._lineStyle

    @lineStyle.setter
    def lineStyle(self, value):
        self._lineStyle = value
        self.lineStyleChanged.emit(value)

    @property
    def lineWidth(self):
        return self._lineWidth

    @lineWidth.setter
    def lineWidth(self, value):
        self._lineWidth = value
        self.lineWidthChanged.emit(value)

    def reset(self):
        self._lineColor = "#000000"
        self._backgroundColor = "#ffffff"
        self._lineStyle = Qt.SolidLine
        self._lineWidth = 3
