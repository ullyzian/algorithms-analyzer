from typing import TYPE_CHECKING

import numpy
import pyqtgraph
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                             QPushButton,
                             QSplitter,
                             QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)
from pyqtgraph import mkPen

if TYPE_CHECKING:
    from app.views import View


class UiMainWindow:
    def __init__(self, MainWindow: "View"):
        self._window = MainWindow

        # Set central widget
        self.centralWidget = QWidget(self._window)
        self.mainLayout = QHBoxLayout(self.centralWidget)
        self._window.setCentralWidget(self.centralWidget)

        # Layouts
        self.presentationLayout = QHBoxLayout()
        self.presentationLayout.addWidget(QLabel())
        self.managementLayout = QVBoxLayout()
        self.managementLayout.setAlignment(Qt.AlignTop)

        # Init presentations
        self.plot = None
        self.table = None

        # Settings label
        self.settingsLabel = StyledLabel("Ustawenia")
        self.settingsLabel.setFont(QFont('Arial', 18))
        self.settingsLabel.setAlignment(Qt.AlignCenter)

        # Settings form

        # Repetitions amount
        self.repetitionsAmountLabel = StyledLabel("Minimalna próba badawcza")
        self.repetitionsAmountInput = StyledInput(str(self._window._model.repetitionsAmount))
        self.repetitionsAmountInput.setValidator(QIntValidator())

        # Max size array
        self.maxSizeLabel = StyledLabel("Maksymalny rozmiar sortowania tablic")
        self.maxSizeInput = StyledInput(str(self._window._model.maxSize))
        self.maxSizeInput.setValidator(QIntValidator())

        # Lower bound
        self.lowerBoundLabel = StyledLabel("Dolna granica predziału wartości elementów")
        self.lowerBoundInput = StyledInput(str(self._window._model.lowerBound))
        self.lowerBoundInput.setValidator(QIntValidator())

        # Upper bound
        self.upperBoundLabel = StyledLabel("Górna granica predziału wartości elementów")
        self.upperBoundInput = StyledInput(str(self._window._model.upperBound))
        self.upperBoundInput.setValidator(QIntValidator())

        # Algorithm combobox
        self.algorithmSelectLabel = StyledLabel("Wybierz algorytmu do analizy")
        self.algorithmSelect = StyledSelect()
        # Select items
        self.algorithmSelect.addItem("Bucket sort", "bucket-sort")
        self.algorithmSelect.addItem("Bubble sort", "bubble-sort")
        self.algorithmSelect.addItem("Insertion sort", "insertion-sort")
        self.algorithmSelect.addItem("Quick sort", "quick-sort")
        self.algorithmSelect.addItem("Selection sort", "selection-sort")

        # Splitter
        self.splitter = QSplitter()

        # Visualization
        self.visualizationLabel = StyledLabel("Wizualizacja")
        self.visualizationLabel.setFont(QFont('Arial', 18))
        self.visualizationLabel.setAlignment(Qt.AlignCenter)
        self.tableBeforeSortButton = StyledButton("Tablica przed sortowaniem")
        self.tableAfterSortButton = StyledButton("Tablica po sortowaniu")
        self.tableBookBeforeSortButton = StyledButton("Sprawdzian przed sortowaniem")
        self.tableBookAfterSortButton = StyledButton("Sprawdzian po sortowaniu")

        # Presentation
        self.presentationLabel = StyledLabel("Prezentacja")
        self.presentationLabel.setFont(QFont('Arial', 18))
        self.presentationLabel.setAlignment(Qt.AlignCenter)
        self.tablePresentationButton = StyledButton("Tabelaryczna prezentacja złożoności")
        self.plotPresentationButton = StyledButton("Graficzna prezentacja złożoności")

        # Add widgets to management layout
        self.managementLayout.addWidget(self.settingsLabel)
        self.managementLayout.addWidget(self.repetitionsAmountLabel)
        self.managementLayout.addWidget(self.repetitionsAmountInput)
        self.managementLayout.addWidget(self.maxSizeLabel)
        self.managementLayout.addWidget(self.maxSizeInput)
        self.managementLayout.addWidget(self.lowerBoundLabel)
        self.managementLayout.addWidget(self.lowerBoundInput)
        self.managementLayout.addWidget(self.upperBoundLabel)
        self.managementLayout.addWidget(self.upperBoundInput)
        self.managementLayout.addWidget(self.algorithmSelectLabel)
        self.managementLayout.addWidget(self.algorithmSelect)
        self.managementLayout.addWidget(self.visualizationLabel)
        self.managementLayout.addWidget(self.tableBeforeSortButton)
        self.managementLayout.addWidget(self.tableAfterSortButton)
        self.managementLayout.addWidget(self.tableBookBeforeSortButton)
        self.managementLayout.addWidget(self.tableBookAfterSortButton)
        self.managementLayout.addWidget(self.presentationLabel)
        self.managementLayout.addWidget(self.tablePresentationButton)
        self.managementLayout.addWidget(self.plotPresentationButton)

        # Add widgets to main layout
        self.mainLayout.addLayout(self.presentationLayout, 5)
        self.mainLayout.addLayout(self.managementLayout, 1)

        # Menubar
        self.menubar = self._window.menuBar()

        # Decorations menu
        self.decorationsMenu = self.menubar.addMenu('&Dekoracje')
        self.decorationsMenu.addAction(self._window.colorLineAction())
        self.decorationsMenu.addAction(self._window.backgroundColorAction())

        # Line style submenu
        self.lineStyleMenu = self.decorationsMenu.addMenu('&Styl linii')
        self.lineStyleMenu.addAction(self._window.solidLineAction())
        self.lineStyleMenu.addAction(self._window.dotLineAction())
        self.lineStyleMenu.addAction(self._window.dashLineAction())
        self.lineStyleMenu.addAction(self._window.dashDotLineAction())

        # Line width submenu
        self.lineWidthMenu = self.decorationsMenu.addMenu('&Grubość linii')
        for i in range(1, 11):
            self.lineWidthMenu.addAction(self._window.lineWidthAction(i))

        # Reset menu
        self.resetMenu = self.menubar.addMenu('&Resetuj')
        self.resetMenu.addAction(self._window.resetAction())

        # Statusbar
        self.statusbar = QStatusBar(self._window)
        self.statusbar.showMessage("Status: Gotowy")
        self.statusbar.setStyleSheet(
            "background-color: #E5E5E5; color: #000000; font-size: 16px;", )
        self.statusbar.setFixedHeight(35)
        self._window.setStatusBar(self.statusbar)

    def createTable(self, data, rows, columns):
        """
        Creates table presentation
        """
        self.presentationLayout.removeWidget(self.plot)
        self.presentationLayout.removeWidget(self.table)
        self.table = TableView(data, rows, columns)
        self.presentationLayout.addWidget(self.table)

    def createPlot(self, data, title, lineColor="#000000", backgroundColor="#ffffff", lineWidth=3,
                   lineStyle=Qt.SolidLine):
        """
        Creates plot presentation
        """
        self.presentationLayout.removeWidget(self.plot)
        self.presentationLayout.removeWidget(self.table)
        self.plot = pyqtgraph.PlotWidget()

        # Plot customizations
        self.plot.setTitle(title, size="20pt")
        self.plot.setLabel('left', "Pomiary")
        self.plot.setLabel('bottom', "Rozmiar")
        self.plot.setBackground(backgroundColor)
        self.plot.showGrid(x=True, y=True)
        self.plot.addLegend()
        self.presentationLayout.addWidget(self.plot)

        # Evaluate string to float type
        self.size = numpy.array(data["size"]).astype(numpy.float)
        self.calculatedTime = numpy.array(data["calculated_time"]).astype(numpy.float)
        self.estimatedTime = numpy.array(data["estimated_time"]).astype(numpy.float)
        self.memory = numpy.array(data["memory"]).astype(numpy.float)

        # Creates 3 graph for
        # X: Calculated time, Y: Size
        calcTimePen = mkPen(color=lineColor, width=lineWidth, style=lineStyle)
        self.plot.plot(self.size, self.calculatedTime, name="Koszt czasowy (pomiar), us",
                       pen=calcTimePen)

        # X: Estimated time, Y: Size
        estimTimePen = mkPen(color="#FF0000", width=lineWidth, style=Qt.SolidLine)
        self.plot.plot(self.size, self.estimatedTime, name="Koszt czasowy (wzór), O(n)",
                       pen=estimTimePen)

        # X: Memory, Y: Size
        memoryPen = pyqtgraph.mkPen(color="#00FF00", width=lineWidth, style=Qt.SolidLine)
        self.plot.plot(self.size, self.memory, name="Koszt pamięci, O(n)", pen=memoryPen)

    def updatePlots(self, lineColor="#000000", backgroundColor="#ffffff", lineWidth=3,
                    lineStyle=Qt.SolidLine):
        if self.plot:
            self.plot.setBackground(backgroundColor)

            calcTimePen = mkPen(color=lineColor, width=lineWidth, style=lineStyle)
            self.plot.plot(self.size, self.calculatedTime, name="Koszt czasowy (pomiar), us",
                           pen=calcTimePen, clear=True)

            estimTimePen = mkPen(color="#FF0000", width=lineWidth, style=Qt.SolidLine)
            self.plot.plot(self.size, self.estimatedTime, name="Koszt czasowy (wzór), O(n)",
                           pen=estimTimePen)

            memoryPen = mkPen(color="#00FF00", width=lineWidth, style=Qt.SolidLine)
            self.plot.plot(self.size, self.memory, name="Koszt pamięci, O(n)", pen=memoryPen)

    def resetPresentation(self):
        if self.plot is not None and self.plot.plotItem is not None:
            self.plot.close()
        if self.table is not None:
            self.table.close()
        self.presentationLayout.removeWidget(self.plot)
        self.presentationLayout.removeWidget(self.table)


class StyledLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(
            "color: #ffffff"
        )


class StyledButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(25)
        self.setStyleSheet(
            "border-radius: 50px; background-color: #FCA311; border: 1px solid #FCA311; color: "
            "#000000; font-size: 14px;"
        )


class StyledInput(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(25)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setStyleSheet(
            "background-color: #ffffff; color: #000000; border-radius: 5px;"
        )


class StyledSelect(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(25)
        self.setStyleSheet(
            "background-color: #E5E5E5; color: #000000; border: 1px solid #E5E5E5; border-radius: 3px;"
        )


class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.setMinimumHeight(300)
        self.setMinimumWidth(400)
        self.setStyleSheet("background-color: #ffffff; color: #000000")
        header = self.horizontalHeader()
        header.setStyleSheet("font-size: 14px;")
        header.setSectionResizeMode(QHeaderView.Stretch)

    def updateTable(self, data):
        self.data = data
        self.setData()

    def setData(self):
        horHeaders = []
        for n, key in enumerate(self.data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newItem = QTableWidgetItem(item)
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(m, n, newItem)
        self.setHorizontalHeaderLabels(horHeaders)
