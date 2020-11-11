from PyQt5.QtCore import QObject, pyqtSlot

from app.models import Model
from app.views import View


class ViewController(QObject):
    def __init__(self, model: Model, view: View):
        super().__init__()
        self._model = model
        self._view = view

        # listen for model event signals
        # View events
        self._view.ui.repetitionsAmountInput.textChanged.connect(self.changeRepetitionsAmount)
        self._view.ui.maxSizeInput.textChanged.connect(self.changeMaxSize)
        self._view.ui.lowerBoundInput.textChanged.connect(self.changeLowerBound)
        self._view.ui.upperBoundInput.textChanged.connect(self.changeUpperBound)
        self._view.ui.algorithmSelect.currentTextChanged.connect(
            lambda: self.changeAlgorithm(self._view.ui.algorithmSelect.currentData())
        )
        self._view.ui.tablePresentationButton.clicked.connect(self.showTable)
        self._view.ui.plotPresentationButton.clicked.connect(self.showPlot)

    @pyqtSlot()
    def showTable(self):
        data, _ = self._model.analyze()
        self._view.ui.createTable(data, len(list(data.values())[0]), len(data))

    @pyqtSlot()
    def showPlot(self):
        data, title = self._model.analyze()
        self._view.ui.createPlot(data, title, lineColor=self._model.decorations.lineColor,
                                 backgroundColor=self._model.decorations.backgroundColor,
                                 lineWidth=self._model.decorations.lineWidth,
                                 lineStyle=self._model.decorations.lineStyle)

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

    @staticmethod
    def defaultParse(value):
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
