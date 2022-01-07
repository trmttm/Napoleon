from ..Interface.interactor import InteractorABC


class ControllersDefault:
    def __init__(self, interactor: InteractorABC):
        self._interactor = interactor
