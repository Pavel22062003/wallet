from models import LoginModel
from services.file_manager import FileManager
from services.wallet.wallet_manager import WalletManager
from services.auth.dataclasses import ShowData


class RegisterManager:
    def __init__(self, data: LoginModel):
        self.data = data

    def create_user(self):
        manager = FileManager(filename='users')
        manager.add_data(income_data=self.data.to_write())
        wallet_manager = WalletManager(hash_id=self.data.hash)
        show_data = ShowData(**wallet_manager.create_wallet())
        print('Вы успешно зарегестрированы')
        for key, value in show_data.to_dict().items():
            print(f'{key} - {value}')
        return show_data
