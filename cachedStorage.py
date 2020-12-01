from database import DataBase


class CachedStorage:
    def __init__(self, main_storage_config, cached_storage):
        self.main_storage_config = main_storage_config
        self.cached_storage = cached_storage

    def get(self, user_id):
        data = self.cached_storage.get(user_id)
        if not data:
            main_bd = DataBase(self.main_storage_config)
            data = main_bd.get(user_id)
            self.cached_storage.update(data)
        return data

    def update(self, user_id=None, new_data=None):
        main_bd = DataBase(self.main_storage_config)
        result = main_bd.update(user_id, new_data)
        if result:
            self.cached_storage.update(user_id, new_data)
        return True


