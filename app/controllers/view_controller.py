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
        self._view.ui.tableBeforeSortButton.clicked.connect(self.arrayBeforeSort)
        self._view.ui.tableAfterSortButton.clicked.connect(self.arrayAfterSort)

    @pyqtSlot()
    def showTable(self):
        data, _ = self._model.analyze()
        self._view.ui.createTable(data, len(list(data.values())[0]), len(data))
        self._view.ui.statusbar.showMessage(
            f"Info: Tablica danych dla algorytmu {self._model.algorithm}")

    @pyqtSlot()
    def showPlot(self):
        data, title = self._model.analyze()
        self._view.ui.createPlot(data, title, lineColor=self._model.decorations.lineColor,
                                 backgroundColor=self._model.decorations.backgroundColor,
                                 lineWidth=self._model.decorations.lineWidth,
                                 lineStyle=self._model.decorations.lineStyle)
        self._view.ui.statusbar.showMessage(f"Info: Grafika dla algorytmu"
                                            f" {self._model.algorithm}")

    @pyqtSlot()
    def arrayBeforeSort(self):
        data = self._model.unsortedArray()
        self._view.ui.createTable(data, len(list(data.values())[0]), len(data))
        self._view.ui.statusbar.showMessage(
            f"Info: Tablica przed sortowaniem {self._model.algorithm}")

    @pyqtSlot()
    def arrayAfterSort(self):
        data = self._model.sortedArray()
        self._view.ui.createTable(data, len(list(data.values())[0]), len(data))
        self._view.ui.statusbar.showMessage(
            f"Info: Tablica po sortowaniu {self._model.algorithm}")

    @pyqtSlot(str)
    def changeRepetitionsAmount(self, value):
        if self.defaultParse(value):
            self._model.repetitionsAmount = int(value)
            self._view.ui.repetitionsAmountInput.setStyleSheet(
                "background-color: #ffffff; color: #000000; border-radius: 5px;"
            )
        else:
            self._view.ui.repetitionsAmountInput.setStyleSheet(
                "background-color: #FF4949; border-radius: 5px;")

    @pyqtSlot(str)
    def changeMaxSize(self, value):
        if self.defaultParse(value):
            self._model.maxSize = int(value)
            self._view.ui.maxSizeInput.setStyleSheet(
                "background-color: #ffffff; color: #000000; border-radius: 5px;"
            )
        else:
            self._view.ui.maxSizeInput.setStyleSheet(
                "background-color: #FF4949; border-radius: 5px;")

    @pyqtSlot(str)
    def changeLowerBound(self, value):
        if self.defaultParse(value):
            if self._model.upperBound <= int(value):
                self._view.ui.statusbar.showMessage(
                    f"Error: Dolna granica musi być mniejsza niż górna granica. "
                    f"{self._model.upperBound} <= {value}")
                self._view.ui.lowerBoundInput.setStyleSheet(
                    "background-color: #FF4949; border-radius: 5px;")
            else:
                self._model.lowerBound = int(value)
                self._view.ui.lowerBoundInput.setStyleSheet(
                    "background-color: #ffffff; color: #000000; border-radius: 5px;"
                )
        else:
            self._view.ui.lowerBoundInput.setStyleSheet(
                "background-color: #FF4949; border-radius: 5px;")

    @pyqtSlot(str)
    def changeUpperBound(self, value):
        if self.defaultParse(value):
            if self._model.lowerBound >= int(value):
                self._view.ui.statusbar.showMessage(
                    f"Error: Górna granica musi być większa niż dolna granica. "
                    f"{self._model.lowerBound} >= {value}")
                self._view.ui.upperBoundInput.setStyleSheet(
                    "background-color: #FF4949; border-radius: 5px;")
            else:
                self._model.upperBound = int(value)
                self._view.ui.upperBoundInput.setStyleSheet(
                    "background-color: #ffffff; color: #000000; border-radius: 5px;"
                )
        else:
            self._view.ui.upperBoundInput.setStyleSheet(
                "background-color: #FF4949; border-radius: 5px;")

    @pyqtSlot(str)
    def changeAlgorithm(self, value):
        if not isinstance(value, str):
            self._view.ui.statusbar.showMessage(f"Error: Otrzymano nietekstowy typ danych '"
                                                f"{type(value)}'")
            self._view.ui.algorithmSelect.setStyleSheet(
                "background-color: #FF4949; border-radius: 5px;")
        elif self._model.algorithmList[value] is None:
            self._view.ui.statusbar.showMessage(f"Error: Otrzymano nieznany alogrytm '{value}'")
            self._view.ui.algorithmSelect.setStyleSheet(
                "background-color: #FF4949; border-radius: 5px;")
        else:
            self._model.algorithm = value
            self._view.ui.statusbar.showMessage(f"Info: Wybrany algorytm '{value}'")
            self._view.ui.algorithmSelect.setStyleSheet(
                "background-color: #ffffff; color: #000000; border-radius: 5px;"
            )

    def defaultParse(self, value):
        if value == '':
            self._view.ui.statusbar.showMessage(f"Error: Otrzymano pusty tekst")
        else:
            value = int(value)
            if value < 1:
                self._view.ui.statusbar.showMessage(f"Error: Wartość musi być większa niż 1. "
                                                    f"Otrymano '{value}'")
                return False
            else:
                return True
