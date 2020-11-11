from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from app.controllers import MainController
from app.models import Model
from app.views.main_view_ui import UiMainWindow


class MainView(QMainWindow):
    def __init__(self, model: Model, main_controller: MainController):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = UiMainWindow()
        self._ui.setupUi(self)

        # listen for model event signals
        self._ui.minSizeRepeatInput.textChanged.connect(
            self._main_controller.changeRepetitionsAmount)
        self._ui.maxSizeRepeatInput.textChanged.connect(
            self._main_controller.changeMaxSize
        )
        self._ui.lowerBoundInput.textChanged.connect(
            self._main_controller.changeLowerBound
        )
        self._ui.upperBoundInput.textChanged.connect(
            self._main_controller.changeUpperBound
        )
        self._ui.algorithmCombobox.currentTextChanged.connect(
            lambda: self._main_controller.changeAlgorithm(self._ui.algorithmCombobox.currentData())
        )
        self._ui.showTablePresentation.clicked.connect(self.showTable)
        self._ui.showPlotPresentation.clicked.connect(self.showPlot)
        self._model.decorations.lineColorChanged.connect(self.onDecorationsChange)
        self._model.decorations.backgroundColorChanged.connect(self.onDecorationsChange)
        self._model.decorations.lineWeightChanged.connect(self.onDecorationsChange)
        self._model.decorations.lineStyleChanged.connect(self.onDecorationsChange)
        self._model.repetitionsAmountChanged.connect(self.onRepetitionsAmountChange)
        self._model.maxSizeChanged.connect(self.onMaxSizeChange)
        self._model.lowerBoundChanged.connect(self.onLowerBoundChange)
        self._model.upperBoundChanged.connect(self.onUpperBoundChange)
        self._model.algorithmChanged.connect(self.onAlgorithmChange)

    @pyqtSlot()
    def showTable(self):
        data, _ = self._model.analyze()
        self._ui.createTable(data, len(list(data.values())[0]), len(data))

    @pyqtSlot()
    def showPlot(self):
        data, title = self._model.analyze()
        self._ui.createPlot(data, title, lineColor=self._model.decorations.lineColor,
                            backgroundColor=self._model.decorations.backgroundColor,
                            lineWeight=self._model.decorations.lineWeight,
                            lineStyle=self._model.decorations.lineStyle)

    @pyqtSlot()
    def reset(self):
        self._model.reset()
        self._ui.resetPresentation()

    @pyqtSlot(int)
    def onRepetitionsAmountChange(self, value):
        self._ui.minSizeRepeatInput.setText(str(value))

    @pyqtSlot(int)
    def onMaxSizeChange(self, value):
        self._ui.maxSizeRepeatInput.setText(str(value))

    @pyqtSlot(int)
    def onLowerBoundChange(self, value):
        self._ui.lowerBoundInput.setText(str(value))

    @pyqtSlot(int)
    def onUpperBoundChange(self, value):
        self._ui.upperBoundInput.setText(str(value))

    @pyqtSlot(str)
    def onAlgorithmChange(self, value):
        self._ui.algorithmCombobox.setCurrentText(value)

    def onDecorationsChange(self):
        self._ui.updatePlots(lineColor=self._model.decorations.lineColor,
                             backgroundColor=self._model.decorations.backgroundColor,
                             lineWeight=self._model.decorations.lineWeight,
                             lineStyle=self._model.decorations.lineStyle)

    def setColorLineAction(self):
        action = QtWidgets.QAction(' &Line color', self)
        action.triggered.connect(self._main_controller.setLineColor)
        return action

    def setBackgroundColorAction(self):
        action = QtWidgets.QAction(' &Background color', self)
        action.triggered.connect(self._main_controller.setBackgroundColor)
        return action

    def setSolidLineAction(self):
        action = QtWidgets.QAction(' &Solid', self)
        action.triggered.connect(lambda: self._main_controller.setLineStyle("solid"))
        return action

    def setDotLineAction(self):
        action = QtWidgets.QAction(' &Dot', self)
        action.triggered.connect(lambda: self._main_controller.setLineStyle("dot"))
        return action

    def setDashDotLineAction(self):
        action = QtWidgets.QAction(' &DashDot', self)
        action.triggered.connect(lambda: self._main_controller.setLineStyle("dash-dot"))
        return action

    def setDashLineAction(self):
        action = QtWidgets.QAction(' &Dash', self)
        action.triggered.connect(lambda: self._main_controller.setLineStyle("dash"))
        return action

    def resetAction(self):
        action = QtWidgets.QAction(' &Reset', self)
        action.triggered.connect(self.reset)
        return action
