from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QAction, QColorDialog, QMainWindow

from app.models import Model
from app.views.ui import UiMainWindow


class View(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.setWindowTitle("Analizator algoritmów")
        self.setStyleSheet("background-color: #0F1108;")
        self.setFixedSize(1000, 600)

        self._model = model
        self.ui = UiMainWindow(self)

    @pyqtSlot()
    def reset(self):
        self._model.reset()
        self.ui.resetPresentation()
        self.ui.repetitionsAmountInput.setText(str(self._model.repetitionsAmount))
        self.ui.maxSizeInput.setText(str(self._model.maxSize))
        self.ui.lowerBoundInput.setText(str(self._model.lowerBound))
        self.ui.upperBoundInput.setText(str(self._model.upperBound))
        self.ui.algorithmSelect.setCurrentIndex(0)
        self.ui.statusbar.showMessage("Status: Wyczyszczone")

    @pyqtSlot()
    def setLineColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self._model.decorations.lineColor = color.name()
            self.ui.statusbar.showMessage(f"Info: Kolor linii został zmeniony na {color.name()}")

    @pyqtSlot()
    def setBackgroundColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self._model.decorations.backgroundColor = color.name()
            self.ui.statusbar.showMessage(f"Info: Kolor tła został zmeniony na {color.name()}")

    @pyqtSlot(str)
    def setLineStyle(self, style):
        styles = {
            "solid": Qt.SolidLine,
            "dot": Qt.DotLine,
            "dash": Qt.DashLine,
            "dash-dot": Qt.DashDotLine
        }
        self._model.decorations.lineStyle = styles[style]
        self.ui.statusbar.showMessage(f"Info: Styl linii został zmeniony na {style}")

    @pyqtSlot(int)
    def setLineWidth(self, width):
        self._model.decorations.lineWidth = int(width)
        self.ui.statusbar.showMessage(f"Info: Grubość linii została zmeniona na {width}")

    def colorLineAction(self):
        action = QAction(' &Kolor linii', self)
        action.triggered.connect(self.setLineColor)
        return action

    def backgroundColorAction(self):
        action = QAction(' &Kolor tła', self)
        action.triggered.connect(self.setBackgroundColor)
        return action

    def solidLineAction(self):
        action = QAction(' &Solid', self)
        action.triggered.connect(lambda: self.setLineStyle("solid"))
        return action

    def dotLineAction(self):
        action = QAction(' &Dot', self)
        action.triggered.connect(lambda: self.setLineStyle("dot"))
        return action

    def dashDotLineAction(self):
        action = QAction(' &DashDot', self)
        action.triggered.connect(lambda: self.setLineStyle("dash-dot"))
        return action

    def dashLineAction(self):
        action = QAction(' &Dash', self)
        action.triggered.connect(lambda: self.setLineStyle("dash"))
        return action

    def lineWidthAction(self, i):
        action = QAction(f' &{i}', self)
        action.triggered.connect(lambda: self.setLineWidth(i))
        return action

    def resetAction(self):
        action = QAction(' &Resetuj', self)
        action.triggered.connect(self.reset)
        return action
