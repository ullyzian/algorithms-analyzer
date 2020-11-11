from typing import Any, Union

from PyQt5.QtCore import QObject, pyqtSignal

from .algorithms import BubbleSort, BucketSort, InsertionSort
from .decorations import Decorations


class Model(QObject):
    """
    Main model for app
    Inherits from QObject to implement PyQt signals/slots mechanism
    """
    repetitionsAmountChanged = pyqtSignal(int)
    maxSizeChanged = pyqtSignal(int)
    lowerBoundChanged = pyqtSignal(int)
    upperBoundChanged = pyqtSignal(int)
    algorithmChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._repetitionsAmount = 20
        self._maxSize = 50
        self._lowerBound = 20
        self._upperBound = 10000
        self._algorithm = "bucket-sort"
        self._algorithmList = {
            "bucket-sort": BucketSort,
            "bubble-sort": BubbleSort,
            "insertion-sort": InsertionSort,
            "quick-sort": 1,
            "selection-sort": 2,
        }
        self.decorations = Decorations()

    @property
    def repetitionsAmount(self) -> int:
        return self._repetitionsAmount

    @repetitionsAmount.setter
    def repetitionsAmount(self, value: int) -> None:
        self._repetitionsAmount = value
        self.repetitionsAmountChanged.emit(value)

    @property
    def maxSize(self) -> int:
        return self._maxSize

    @maxSize.setter
    def maxSize(self, value: int) -> None:
        self._maxSize = value
        self.maxSizeChanged.emit(value)

    @property
    def lowerBound(self) -> int:
        return self._lowerBound

    @lowerBound.setter
    def lowerBound(self, value):
        self._lowerBound = value
        self.lowerBoundChanged.emit(value)

    @property
    def upperBound(self) -> int:
        return self._upperBound

    @upperBound.setter
    def upperBound(self, value: int) -> None:
        self._upperBound = value
        self.upperBoundChanged.emit(value)

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        self._algorithm = value
        self.algorithmChanged.emit(value)

    @property
    def algorithmList(self) -> dict:
        return self._algorithmList

    def analyze(self) -> Union[Any, Any]:
        algorithm = self.algorithmList[self.algorithm](self.lowerBound, self.upperBound,
                                                       self.maxSize, self.repetitionsAmount)
        return algorithm.calculate(), algorithm.__repr__()

    def reset(self) -> None:
        self._repetitionsAmount = 20
        self._maxSize = 50
        self._lowerBound = 20
        self._upperBound = 10000
        self._algorithm = "bucket-sort"
        self.decorations.reset()
        print("Reseted")
