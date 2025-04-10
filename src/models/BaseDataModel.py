from helpers.config import get_settings,Settings

class BaseDataModel:
    def __init__(self, db_clint: object):
        self.db_client=db_clint
        self.app_settings = get_settings()
        