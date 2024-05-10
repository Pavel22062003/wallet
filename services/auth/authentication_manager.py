from models import LoginModel
from services.file_manager import FileManager, SearchData
from services.auth.dataclasses import ShowData, ProfileData
from services.wallet.wallet_manager import WalletManager


class AuthenticationManager:
    def __init__(self, data: LoginModel):
        self.data = data

    def check_auth(self):
        manager = FileManager(filename='users')
        search_data = SearchData(key='password', value=self.data.to_hash())
        instance = manager.find_instance(search_data)
        if instance:
            user_data = LoginModel(**instance)
            wallet_manager = WalletManager(hash_id=instance.get('password'))
            show_data = ShowData(**wallet_manager.get_wallet())
            print('Вы успешно вошли')
            print('Ваш кошелек')
            for key, value in show_data.to_dict().items():
                print(f'{key} - {value}')
            profile_data = ProfileData()
            profile_data.set_data(profile_data=user_data, wallet_data=show_data)
            return profile_data
        return None
