from services.auth.authentication_manager import AuthenticationManager
from services.auth.register_manager import RegisterManager
from models import LoginModel
from services.auth.dataclasses import ProfileData

class AuthInterface:
    def __init__(self, retry=False):
        self.retry = retry

    def process(self):
        if self.retry:
            print('Пользователь с такими учетными данными не найден')
        print(f'Зарегестрироваться - 1')
        print(f'Войти - 2')
        step = int(input('Введите цфиру'))
        if step == 1:
            data = self.input_data()
            register_manager = RegisterManager(data=data)
            wallet_data = register_manager.create_user()
            profile_data = ProfileData()
            profile_data.set_data(profile_data=data, wallet_data=wallet_data)
            return profile_data
        else:
            return self.auth()

    @staticmethod
    def input_data():
        username = input('Введите логин')
        password = input('Введите пароль')
        model = LoginModel(username=username, password=password)
        model.to_hash()
        return model

    def auth(self):
        data = self.input_data()
        manager = AuthenticationManager(data=data)
        hash_id = manager.check_auth()
        if not hash_id:
            return AuthInterface(retry=True).process()
        return hash_id
