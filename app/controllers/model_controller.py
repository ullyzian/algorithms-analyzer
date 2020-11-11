from PyQt5.QtCore import QObject, pyqtSlot

from app.models import Model
from app.views import View


class ModelController(QObject):
    def __init__(self, model: Model, view: View):
        super().__init__()
        self._model = model
        self._view = view

        self._model.decorations.lineColorChanged.connect(self.onDecorationsChange)
        self._model.decorations.backgroundColorChanged.connect(self.onDecorationsChange)
        self._model.decorations.lineWidthChanged.connect(self.onDecorationsChange)
        self._model.decorations.lineStyleChanged.connect(self.onDecorationsChange)
        self._model.repetitionsAmountChanged.connect(self.onRepetitionsAmountChange)
        self._model.maxSizeChanged.connect(self.onMaxSizeChange)
        self._model.lowerBoundChanged.connect(self.onLowerBoundChange)
        self._model.upperBoundChanged.connect(self.onUpperBoundChange)
        self._model.algorithmChanged.connect(self.onAlgorithmChange)

    @pyqtSlot(int)
    def onRepetitionsAmountChange(self, value):
        self._view.ui.repetitionsAmountInput.setText(str(value))

    @pyqtSlot(int)
    def onMaxSizeChange(self, value):
        self._view.ui.maxSizeInput.setText(str(value))

    @pyqtSlot(int)
    def onLowerBoundChange(self, value):
        self._view.ui.lowerBoundInput.setText(str(value))

    @pyqtSlot(int)
    def onUpperBoundChange(self, value):
        self._view.ui.upperBoundInput.setText(str(value))

    @pyqtSlot(str)
    def onAlgorithmChange(self, value):
        self._view.ui.algorithmSelect.setCurrentText(value)

    def onDecorationsChange(self):
        self._view.ui.updatePlots(lineColor=self._model.decorations.lineColor,
                                  backgroundColor=self._model.decorations.backgroundColor,
                                  lineWidth=self._model.decorations.lineWidth,
                                  lineStyle=self._model.decorations.lineStyle)
