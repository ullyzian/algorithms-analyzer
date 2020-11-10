from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from app.controllers.main_controller import MainController
from app.models.model import Model
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

    @pyqtSlot(bool)
    def on_enable_reset_changed(self, value):
        # self._ui.pushButton_reset.setEnabled(value)
        pass

    def showTable(self):
        data, _ = self._model.analyze()
        self._ui.createTable(data, len(list(data.values())[0]), len(data))

    def showPlot(self):
        data, title = self._model.analyze()
        self._ui.createPlot(data, title)

    def setColorLineAction(self):
        action = QtWidgets.QAction(' &Line color', self)
        action.triggered.connect(self.openColorDialog)
        return action

    def setSolidLineAction(self):
        action = QtWidgets.QAction(' &Solid', self)
        action.triggered.connect(partial(print, "Solid selected"))
        return action

    def setDotLineAction(self):
        action = QtWidgets.QAction(' &Dot', self)
        action.triggered.connect(partial(print, "Dot selected"))
        return action

    def setDashDotLineAction(self):
        action = QtWidgets.QAction(' &DashDot', self)
        action.triggered.connect(partial(print, "DashDot selected"))
        return action

    def setDashLineAction(self):
        action = QtWidgets.QAction(' &Dash', self)
        action.triggered.connect(partial(print, "Dash selected"))
        return action

    def setBackgroundColorAction(self):
        action = QtWidgets.QAction(' &Background color', self)
        action.triggered.connect(self.openColorDialog)
        return action

    def resetAction(self):
        action = QtWidgets.QAction(' &Reset', self)
        action.triggered.connect(self._model.reset)
        return action

    def openColorDialog(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            print(color.name())
