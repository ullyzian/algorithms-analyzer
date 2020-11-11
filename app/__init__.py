from PyQt5.QtWidgets import QApplication

from app.controllers import Controller
from app.models import Model
from app.views import View


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.view = View(self.model)
        self.controller = Controller(self.model, self.view)
        self.view.show()
