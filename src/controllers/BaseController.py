from helpers.config import BaseSettings,get_settings
class BaseController:
    def __init__(self):
        self.app_settings=get_settings()
        