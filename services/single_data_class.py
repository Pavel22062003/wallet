from dataclasses import dataclass
from enum import Enum
from services.auth.dataclasses import ProfileData
from models import ChangeDataModel

class DataType(Enum):
    profile_info = 'profile_info'
    changes_info = 'changes_info'

@dataclass
class UserDataClass:
    profile_info: ProfileData | None = None
    changes_info: list[ChangeDataModel] | None = None


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance


class UserDataManager(Singleton):
    def __init__(self):
        self.user_data = UserDataClass()

    def set_data(self, data, data_type):
        setattr(self.user_data, data_type.value, data)
