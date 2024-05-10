from services.auth.auth_interface import AuthInterface
from services.single_data_class import UserDataManager, DataType
from services.wallet.wallet_manager import WalletManager
from services.wallet.wallet_interface import WalletInterface
from threading import Thread

if __name__ == '__main__':
    auth_interface = AuthInterface()
    user_profile_data = auth_interface.process()
    user_data_manager = UserDataManager()
    user_data_manager.set_data(data=user_profile_data, data_type=DataType.profile_info)
    wallet_manager = WalletManager(user_data_manager.user_data.profile_info.password)
    thread = Thread(target=wallet_manager.load_changes, kwargs={'user_data_manager': user_data_manager})
    thread.start()
    while True:
        print('Доступные действия')
        print('1 - мой баланс')
        print('2 - Перейти в раздел изменнеий баланса')
        step = int(input('Введите цифру'))
        if step == 1:
            for key, value in user_data_manager.user_data.profile_info.get_wallet_data().items():
                print(f'{key} - {value}')
        if step == 2:
            wallet_interface = WalletInterface(wallet_manager, user_data_manager)
            wallet_interface.process()
