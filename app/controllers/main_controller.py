from PyQt5.QtCore import QObject, pyqtSlot

from app.models.model import Model


class MainController(QObject):
    def __init__(self, model: Model):
        super().__init__()

        self._model = model

    @pyqtSlot(int)
    def change_amount(self, value):
        self._model.amount = value

        # calculate even or odd
        self._model.even_odd = 'odd' if value % 2 else 'even'

        # calculate button enabled state
        self._model.enable_reset = True if value else False

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

    def changeRepetitionsAmount(self, value):
        if self.defaultParse(value):
            self._model.repetitionsAmount = int(value)

    def changeMaxSize(self, value):
        if self.defaultParse(value):
            self._model.maxSize = int(value)

    def changeLowerBound(self, value):
        if self.defaultParse(value):
            if self._model.upperBound <= int(value):
                print("Lower bound must be less than upper bound")
            else:
                self._model.lowerBound = int(value)

    def changeUpperBound(self, value):
        if self.defaultParse(value):
            if self._model.lowerBound >= int(value):
                print("Upper bound must be greater than lower bound")
            else:
                self._model.upperBound = int(value)

    def changeAlgorithm(self, value):
        if not isinstance(value, str):
            print("Given non str type")
        elif self._model.algorithmList[value] is None:
            print("Unknown algorithm given")
        else:
            self._model.algorithm = value
