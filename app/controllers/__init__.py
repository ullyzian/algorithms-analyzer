from PyQt5.QtCore import QObject

from app.controllers.model_controller import ModelController
from app.controllers.view_controller import ViewController
from app.models import Model
from app.views import View


class Controller(QObject):
    def __init__(self, model: Model, view: View):
        super().__init__()
        self._model = model
        self._view = view
        self.vController = ViewController(self._model, self._view)
        self.mController = ModelController(self._model, self._view)
