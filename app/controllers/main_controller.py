from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot

from app.models.model import Model


class MainController(QObject):
    def __init__(self, model: Model):
        super().__init__()

        self._model = model

    @pyqtSlot()
    def setLineColor(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self._model.decorations.lineColor = color.name()

    @pyqtSlot()
    def setBackgroundColor(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self._model.decorations.backgroundColor = color.name()

    @pyqtSlot(str)
    def setLineStyle(self, style):
        styles = {
            "solid": QtCore.Qt.SolidLine,
            "dot": QtCore.Qt.DotLine,
            "dash": QtCore.Qt.DashLine,
            "dash-dot": QtCore.Qt.DashDotLine
        }
        self._model.decorations.lineStyle = styles[style]

    @pyqtSlot(int)
    def setLineWeight(self, weight):
        self._model.decorations.lineWeight = weight

    def defaultParse(self, value):
        if value == '':
            print("Given empty value")
            return False
        else:
            value = int(value)
            if value < 1:
                print("Value must be greater than 1")
                return False
            else:
                return True

    @pyqtSlot(str)
    def changeRepetitionsAmount(self, value):
        if self.defaultParse(value):
            self._model.repetitionsAmount = int(value)


    @pyqtSlot(str)
    def changeMaxSize(self, value):
        if self.defaultParse(value):
            self._model.maxSize = int(value)

    @pyqtSlot(str)
    def changeLowerBound(self, value):
        if self.defaultParse(value):
            if self._model.upperBound <= int(value):
                print("Lower bound must be less than upper bound")
            else:
                self._model.lowerBound = int(value)

    @pyqtSlot(str)
    def changeUpperBound(self, value):
        if self.defaultParse(value):
            if self._model.lowerBound >= int(value):
                print("Upper bound must be greater than lower bound")
            else:
                self._model.upperBound = int(value)

    @pyqtSlot(str)
    def changeAlgorithm(self, value):
        if not isinstance(value, str):
            print("Given non str type")
        elif self._model.algorithmList[value] is None:
            print("Unknown algorithm given")
        else:
            self._model.algorithm = value
