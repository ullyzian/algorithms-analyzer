from typing import TYPE_CHECKING

import numpy
import pyqtgraph
from PyQt5 import QtCore, QtGui, QtWidgets

if TYPE_CHECKING:
    from app.views.main_view import MainView


class UiMainWindow:
    def setupUi(self, MainWindow: "MainView"):
        self._window = MainWindow
        self._window.setWindowTitle("Analizator algoritmów")
        self._window.setFixedSize(1000, 600)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(self._window)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self._window.setCentralWidget(self.centralwidget)

        # Layouts
        self.presentationLayout = QtWidgets.QHBoxLayout()
        self.presentationLayout.addWidget(QtWidgets.QLabel())
        self.managmentLayout = QtWidgets.QVBoxLayout()
        self.managmentLayout.setAlignment(QtCore.Qt.AlignTop)

        # Init presentations
        self.graph = None
        self.table = None


        # Settings
        self.settingsLabel = QtWidgets.QLabel("Ustawenia")
        self.settingsLabel.setFont(QtGui.QFont('Arial', 18))
        self.settingsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.minSizeRepeatLabel = QtWidgets.QLabel("Minimalna próba badawcza")
        self.minSizeRepeatInput = QtWidgets.QLineEdit(str(self._window._model.repetitionsAmount))
        self.minSizeRepeatInput.setValidator(QtGui.QIntValidator())
        self.maxSizeRepeatLabel = QtWidgets.QLabel("Maksymalny rozmiar sortowania tablic")
        self.maxSizeRepeatInput = QtWidgets.QLineEdit(str(self._window._model.maxSize))
        self.maxSizeRepeatInput.setValidator(QtGui.QIntValidator())
        self.lowerBoundLabel = QtWidgets.QLabel("Dolna granica predziału wartości elementów")
        self.lowerBoundInput = QtWidgets.QLineEdit(str(self._window._model.lowerBound))
        self.lowerBoundInput.setValidator(QtGui.QIntValidator())
        self.upperBoundLabel = QtWidgets.QLabel("Górna granica predziału wartości elementów")
        self.upperBoundInput = QtWidgets.QLineEdit(str(self._window._model.upperBound))
        self.upperBoundInput.setValidator(QtGui.QIntValidator())
        self.algorithmComboboxLabel = QtWidgets.QLabel("Wybierz algorytmu do analizy")
        self.algorithmCombobox = QtWidgets.QComboBox()
        self.algorithmCombobox.addItem("Bucket sort", "bucket-sort")
        self.algorithmCombobox.addItem("Bubble sort", "bubble-sort")
        self.algorithmCombobox.addItem("Insertion sort", "insertion-sort")
        self.algorithmCombobox.addItem("Quick sort", "quick-sort")
        self.algorithmCombobox.addItem("Selection sort", "selection-sort")
        self.splitter = QtWidgets.QSplitter()

        # Visualization
        self.visualizationLabel = QtWidgets.QLabel("Wizualizacja")
        self.visualizationLabel.setFont(QtGui.QFont('Arial', 18))
        self.visualizationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.showTableBeforeSort = QtWidgets.QPushButton("Wizualizacja tablicy przed sortowaniu")
        self.showTableAfterSort = QtWidgets.QPushButton("Wizualizacja tablicy po sortowaniu")

        # Presentation
        self.presentationLabel = QtWidgets.QLabel("Prezentacja")
        self.presentationLabel.setFont(QtGui.QFont('Arial', 18))
        self.presentationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.showTablePresentation = QtWidgets.QPushButton("Tabelaryczna prezentacja złożoności")
        self.showPlotPresentation = QtWidgets.QPushButton("Graficzna prezentacja złożoności")

        # Add widgets to managment layout
        self.managmentLayout.addWidget(self.settingsLabel)
        self.managmentLayout.addWidget(self.minSizeRepeatLabel)
        self.managmentLayout.addWidget(self.minSizeRepeatInput)
        self.managmentLayout.addWidget(self.maxSizeRepeatLabel)
        self.managmentLayout.addWidget(self.maxSizeRepeatInput)
        self.managmentLayout.addWidget(self.lowerBoundLabel)
        self.managmentLayout.addWidget(self.lowerBoundInput)
        self.managmentLayout.addWidget(self.upperBoundLabel)
        self.managmentLayout.addWidget(self.upperBoundInput)
        self.managmentLayout.addWidget(self.algorithmComboboxLabel)
        self.managmentLayout.addWidget(self.algorithmCombobox)
        self.managmentLayout.addWidget(self.splitter)
        self.managmentLayout.addWidget(self.visualizationLabel)
        self.managmentLayout.addWidget(self.showTableBeforeSort)
        self.managmentLayout.addWidget(self.showTableAfterSort)
        self.managmentLayout.addWidget(self.splitter)
        self.managmentLayout.addWidget(self.presentationLabel)
        self.managmentLayout.addWidget(self.showTablePresentation)
        self.managmentLayout.addWidget(self.showPlotPresentation)

        # Add widgets to main layout
        self.mainLayout.addLayout(self.presentationLayout, 5)
        self.mainLayout.addLayout(self.managmentLayout, 1)

        # Menubar
        self.menubar = self._window.menuBar()

        # Decorations menu
        self.decorationsMenu = self.menubar.addMenu('&Decorations')
        self.decorationsMenu.addAction(self._window.setColorLineAction())
        self.decorationsMenu.addAction(self._window.setBackgroundColorAction())

        # Line style submenu
        self.lineStyleMenu = self.decorationsMenu.addMenu('&Line style')
        self.lineStyleMenu.addAction(self._window.setSolidLineAction())
        self.lineStyleMenu.addAction(self._window.setDotLineAction())
        self.lineStyleMenu.addAction(self._window.setDashLineAction())
        self.lineStyleMenu.addAction(self._window.setDashDotLineAction())

        # Reset menu
        self.resetMenu = self.menubar.addMenu('&Reset')
        self.resetMenu.addAction(self._window.resetAction())

        # Statusbar
        self.statusbar = QtWidgets.QStatusBar(self._window)
        self._window.setStatusBar(self.statusbar)

    def createTable(self, data, rows, columns):
        """
        Creates table presentation
        """
        self.presentationLayout.removeWidget(self.graph)
        self.presentationLayout.removeWidget(self.table)
        self.table = TableView(data, rows, columns)
        self.presentationLayout.addWidget(self.table)

    def createPlot(self, data, title, lineColor="#000000", backgroundColor="#ffffff", lineWeight=3,
                   lineStyle=QtCore.Qt.SolidLine):
        """
        Creates plot presentation
        """
        self.presentationLayout.removeWidget(self.graph)
        self.presentationLayout.removeWidget(self.table)
        self.graph = pyqtgraph.PlotWidget()

        # Plot customizations
        self.graph.setTitle(title, size="20pt")
        self.graph.setLabel('left', "Pomiary")
        self.graph.setLabel('bottom', "Rozmiar")
        self.graph.setBackground(backgroundColor)
        self.graph.showGrid(x=True, y=True)
        self.graph.addLegend()
        self.presentationLayout.addWidget(self.graph)

        # Evaluate string to float type
        self.size = numpy.array(data["size"]).astype(numpy.float)
        self.calculatedTime = numpy.array(data["calculated_time"]).astype(numpy.float)
        self.estimatedTime = numpy.array(data["estimated_time"]).astype(numpy.float)
        self.memory = numpy.array(data["memory"]).astype(numpy.float)

        # Creates 3 graph for
        # X: Calculated time, Y: Size
        # X: Estimated time, Y: Size
        # X: Memory, Y: Size
        self.calcTimePen = pyqtgraph.mkPen(color=lineColor, width=lineWeight, style=lineStyle)
        self.calcTimePlot = self.graph.plot(self.size, self.calculatedTime,
                                            name="Koszt czasowy (pomiar), us",
                                            pen=self.calcTimePen)
        self.estimTimePen = pyqtgraph.mkPen(color="#FF0000", width=lineWeight,
                                            style=QtCore.Qt.SolidLine)
        self.estimTimePlot = self.graph.plot(self.size, self.estimatedTime,
                                             name="Koszt czasowy (wzór), O(n)",
                                             pen=self.estimTimePen)
        self.memoryPen = pyqtgraph.mkPen(color="#00FF00", width=lineWeight,
                                         style=QtCore.Qt.SolidLine)
        self.memoryPlot = self.graph.plot(self.size, self.memory, name="Koszt pamięci, O(n)",
                                          pen=self.memoryPen)

    def updatePlots(self, lineColor="#000000", backgroundColor="#ffffff", lineWeight=3,
                    lineStyle=QtCore.Qt.SolidLine):
        self.graph.setBackground(backgroundColor)
        self.calcTimePen = pyqtgraph.mkPen(color=lineColor, width=lineWeight, style=lineStyle)
        self.estimTimePen = pyqtgraph.mkPen(color="#FF0000", width=lineWeight,
                                            style=QtCore.Qt.SolidLine)
        self.memoryPen = pyqtgraph.mkPen(color="#00FF00", width=lineWeight,
                                         style=QtCore.Qt.SolidLine)

        self.calcTimePlot = self.graph.plot(self.size, self.calculatedTime,
                                            name="Koszt czasowy (pomiar), us",
                                            pen=self.calcTimePen,
                                            clear=True)

        self.estimTimePlot = self.graph.plot(self.size, self.estimatedTime,
                                             name="Koszt czasowy (wzór), O(n)",
                                             pen=self.estimTimePen)
        self.memoryPlot = self.graph.plot(self.size, self.memory, name="Koszt pamięci, O(n)",
                                          pen=self.memoryPen)

    def resetPresentation(self):
        if self.graph is not None and self.graph.plotItem is not None:
            self.graph.close()
        if self.table is not None:
            self.table.close()
        self.presentationLayout.removeWidget(self.graph)
        self.presentationLayout.removeWidget(self.table)


class TableView(QtWidgets.QTableWidget):
    def __init__(self, data, *args):
        QtWidgets.QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.setMinimumHeight(300)
        self.setMinimumWidth(400)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def updateTable(self, data):
        self.data = data
        self.setData()

    def setData(self):
        horHeaders = []
        for n, key in enumerate(self.data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
