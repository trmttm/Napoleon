from ..Interface.presenter import PresentersABC


class PresentersDefault(PresentersABC):
    def present_setting_screen(self, **current_settings):
        print(f'<Setting Screen>\n{current_settings}\n\nHow many players?')
