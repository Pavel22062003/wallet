import json
from dataclasses import dataclass


@dataclass
class SearchData:
    key: str
    value: str


class FileManager:

    def __init__(self, filename):
        self.filename = filename

    def read_json(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def write_json(self, data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def find_instance(self, search_data: SearchData) -> dict:
        data = self.read_json()
        instance = next((item for item in data if item.get(search_data.key) == search_data.value), None)
        return instance

    def update_instance(self, search_data: SearchData, new_data: dict):
        data = self.read_json()
        instance: dict = next((item for item in data if item.get(search_data.key) == search_data.value), None)
        if instance:
            instance.update(new_data)
            self.write_json(data)

    def add_data(self, income_data: dict):
        file_data = self.read_json()
        file_data.append(income_data)
        self.write_json(data=file_data)

#     def add_or_update_entry(self, search_data: SearchData):
#         data = self.read_json()
#         instance = next((item for item in data if item.get(search_data.key) == search_data.value), None)
#         return instance
#         # if not instance:
#         #     retur
#         # for entry in data:
#         #     instance = data.get(key)
#         #     if entry.get("id") == entry_id:
#         #         entry.update(entry_data)
#         #         break
#         # else:
#         #     # Если запись с таким ID не найдена, добавляем новую запись
#         #     data.append(entry_data)
#
#     else:
#     # Если ID отсутствует, просто добавляем новую запись
#     data.append(entry_data)
#
#
# write_json(data, filename)
