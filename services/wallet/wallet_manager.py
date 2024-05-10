from datetime import datetime
from services.file_manager import FileManager, SearchData
from models import ChangeDataModel
from services.single_data_class import UserDataManager, DataType


class WalletManager:
    def __init__(self, hash_id: str | None = None):
        self.hash = hash_id

    def create_wallet(self) -> dict:
        created_at = datetime.now().isoformat()
        updated_at = datetime.now().isoformat()
        data = {
            'user_id': self.hash,
            'balance': 0,
            'created_at': created_at,
            'updated_at': updated_at,
        }
        manager = FileManager(filename='wallets')
        manager.add_data(income_data=data)
        data['created_at'] = datetime.fromisoformat(created_at)
        data['updated_at'] = datetime.fromisoformat(updated_at)
        return data

    def get_wallet(self) -> dict:
        file_manager = FileManager(filename='wallets')
        wallet = file_manager.find_instance(SearchData(key='user_id', value=self.hash))
        return wallet

    @staticmethod
    def get_data():
        date = input('Введите дату изменения в формaтe 01.01.2000')
        category = input('Введите категорию, можно выбрать либо Доходы, либо Расходы')
        amount = int(input('Введите сумму'))
        description = input('Введите описание')
        return {
            'date': date,
            'category': category,
            'amount': amount,
            'description': description
        }

    def set_change(self, user_data_manager: UserDataManager):
        is_valid = False
        change_data = None
        while not is_valid:
            data = self.get_data()
            try:
                change_data = ChangeDataModel(**data)
                is_valid = True
            except Exception as e:
                print(e)
        user_data_manager.user_data.changes_info.append(change_data)
        data = change_data.dict()
        data['user_id'] = self.hash
        file_manager = FileManager(filename='changes')
        file_manager.add_data(data)
        self.update_balance(user_data_manager=user_data_manager, category=change_data.category,
                            amount=change_data.amount)

    def load_changes(self, user_data_manager: UserDataManager):
        file_manager = FileManager(filename='changes')
        changes = file_manager.read_json()
        if not changes:
            user_data_manager.set_data(data=changes, data_type=DataType.changes_info)
        else:
            data = [ChangeDataModel(**v) for v in changes if v.get('user_id') == self.hash]
            user_data_manager.set_data(data=data, data_type=DataType.changes_info)

    def update_balance(self, user_data_manager: UserDataManager, category, amount):
        if category == 'доходы':
            user_data_manager.user_data.profile_info.balance += amount
        else:
            user_data_manager.user_data.profile_info.balance -= amount
        now = datetime.now()
        user_data_manager.user_data.profile_info.updated_at = now.isoformat()
        wallet_data = user_data_manager.user_data.profile_info.wallet_data_to_save()
        file_manager = FileManager(filename='wallets')
        file_manager.update_instance(search_data=SearchData(key='user_id', value=self.hash), new_data=wallet_data)

    @staticmethod
    def update_change(instance: ChangeDataModel):
        file_manager = FileManager(filename='changes')
        file_manager.update_instance(search_data=SearchData(key='uuid', value=instance.uuid), new_data=instance.dict())

    def filter_instances(self, search_data: SearchData, user_data_manager: UserDataManager):
        changes = user_data_manager.user_data.changes_info
        matches = [v for v in changes if getattr(v, search_data.key) == search_data.value]
        return matches
