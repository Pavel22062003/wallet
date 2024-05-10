import typing
from typing import Any

from pydantic import BaseModel, field_validator
import hashlib
from datetime import datetime
from uuid import uuid4

from pydantic.main import IncEx


class LoginModel(BaseModel):
    username: str
    password: str
    hash: str = None

    def to_hash(self):
        value = self.username + self.password
        value_bytes = str(value).encode('utf-8')
        hash_object = hashlib.sha256(value_bytes)
        self.hash = hash_object.hexdigest()
        return self.hash

    def to_write(self):
        return {
            'username': self.username,
            'password': self.hash
        }


class ChangeDataModel(BaseModel):
    uuid: str = str(uuid4())
    date: str
    category: str
    amount: int
    description: str
    user_id: str | None = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str):
        try:
            datetime.strptime(v, '%d.%m.%Y')
            return v
        except ValueError:
            raise ValueError('must be in format 01.01.2000')

    @field_validator('category')
    @classmethod
    def validate_change_type(cls, v: str):
        if v.lower() not in ['доходы', 'расходы']:
            raise ValueError('Можно выбрать либо Доходы, либо Расходы')
        else:
            return v.lower()

    def to_show(self):
        return {
            'дата': self.date,
            'категория': self.category,
            'сумма': self.amount,
            'описание': self.description,
            'uuid': self.uuid
        }



