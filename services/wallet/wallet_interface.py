from services.file_manager import SearchData
from services.wallet.wallet_manager import WalletManager
from services.single_data_class import UserDataManager, DataType


class WalletInterface:
    def __init__(self, wallet_manager: WalletManager, user_data_manager: UserDataManager):
        self.wallet_manager = wallet_manager
        self.user_data_manager = user_data_manager

    def process(self):
        run = True
        while run:
            print('доступные действия')
            print('1 - изменить баланс')
            print('2 - история изменеия баланса')
            print('3 - редактировать изменение')
            print('4 - найти записи')
            print('5 - назад')
            step = int(input('Введите цифру'))
            if step == 1:
                self.wallet_manager.set_change(self.user_data_manager)
            if step == 2:
                self.show_change_history()
            elif step == 3:
                self.manage_update_changes()
            elif step == 4:
                self.find_changes()
            elif step == 5:
                run = False

    def show_change_history(self):
        for change in self.user_data_manager.user_data.changes_info:
            if change:
                for key, value in change.to_show().items():
                    print(f'{key} - {value}')
                print()
            else:
                print('Нет изменений')

    def manage_update_changes(self):
        self.show_change_history()
        run = True
        while run:
            uuid = input('Введите uuid записи')
            if not uuid.strip():
                print('это поле обязательно')
            else:
                run = False

        instance = next((v for v in self.user_data_manager.user_data.changes_info if v.uuid == uuid), None)
        date = input(
            f'Введите дату изменения в формaтe 01.01.2000, если дата прежняя то нажмите Enter,  прежнее значение - {instance.date}')
        category = input(
            f'Введите категорию, можно выбрать либо Доходы, либо Расходы, если категория прежняя то нажмите Enter,  прежнее значение - {instance.category}')
        amount = int(
            input(f'Введите сумму, если сумма прежняя то нажмите Enter,  прежнее значение - {instance.amount}'))
        description = input(
            f'Введите описание, если описание прежнее то нажмите Enter, прежнее значение - {instance.description}')
        if instance:
            instance.date = date if date.strip() else instance.date
            instance.category = category if category.strip() else instance.category
            instance.amount = amount if amount else instance.amount
            instance.description = description if description.strip() else instance.description
            self.wallet_manager.update_change(instance)

            self.wallet_manager.update_balance(user_data_manager=self.user_data_manager, category=instance.category,
                                               amount=instance.amount)

    def find_changes(self):
        print('Выберите параметр')
        print('1 - дата')
        print('2 - сумма')
        print('3 - категория')
        step = int(input('Введите цифру'))
        value = input('Введите значение')
        if step == 1:
            step = 'date'
        if step == 2:
            step = 'amount'
            value = int(value)
        if step == 3:
            step = 'category'
        result = self.wallet_manager.filter_instances(search_data=SearchData(key=step, value=value),
                                                      user_data_manager=self.user_data_manager)
        if not result:
            print('Ничего не найдено')
            return
        for item in result:
            for key, value in item.to_show().items():
                print(f'{key} - {value}')
            print()
