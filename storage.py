from datetime import datetime, timedelta


class Storage:
    def __init__(self, inner_storage):
        self.time_for_status = 5
        self.status_online = "online"
        self.status_offline = "offline"
        self.inner_storage = inner_storage

    def check_status(self, user_time):
        if user_time + timedelta(
                minutes=self.time_for_status) < datetime.now():
            return self.status_online
        else:
            return self.status_offline

    def get(self, user_id):
        user_time = self.inner_storage.get(user_id)[1]
        return user_id, self.check_status(user_time)

    def update(self, user_id, new_user_time):
        if self.inner_storage.update(user_id, new_user_time):
            return user_id, self.status_online
