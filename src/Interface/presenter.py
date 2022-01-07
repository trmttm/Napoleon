import abc


class PresentersABC(abc.ABC):
    @abc.abstractmethod
    def present_setting_screen(self, **current_settings):
        pass
