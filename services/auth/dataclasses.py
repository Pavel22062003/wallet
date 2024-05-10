from dataclasses import dataclass
from datetime import datetime
from models import LoginModel


@dataclass
class ShowData:
    balance: int
    created_at: datetime
    updated_at: datetime
    user_id: str | None = None

    def to_dict(self):
        return {
            'баланс': self.balance,
            'дата создания': self.created_at,
            'дата обновления': self.updated_at
        }


@dataclass
class ProfileData:
    username: str | None = None
    password: str | None = None
    balance: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def set_data(self, profile_data: LoginModel, wallet_data: ShowData):
        self.username = profile_data.username
        self.password = profile_data.password
        self.balance = wallet_data.balance
        self.created_at = wallet_data.created_at
        self.updated_at = wallet_data.updated_at

    def get_profile_data(self):
        return {
            'Имя пользователя': self.username,
            'Пароль': self.password
        }

    def get_wallet_data(self):
        return {
            'баланс': self.balance,
            'дата создания': self.created_at,
            'дата обновления': self.updated_at
        }

    def wallet_data_to_save(self):
        return {
            'balance': self.balance,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
