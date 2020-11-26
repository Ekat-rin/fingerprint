from datetime import datetime, timedelta
from database import DataBase
from hashlib import sha256
import redis


# Class for work with diffrient data store

class Storage:
    def __init__(self):
        self.time_for_status = 5
        self.red = redis.Redis()
        self.status_online = "online"
        self.status_offline = "offline"

    def check_status(self, user_time):
        if user_time + timedelta(
                minutes=self.time_for_status) < datetime.now():
            return self.status_online
        else:
            return self.status_offline

    # work with cash
    def get_time_from_redis(self, user_id):
        return self.red.get(user_id)

    def add_user_to_redis(self, user_id, user_time):
        self.red.set(user_id, user_time)

    # work with bd table user_id
    def get_time_in_user_id_from_db(self, user_id):
        db = DataBase()
        time = db.get_last_time_from_last_online_time(user_id)[0][1]
        return time

    def update_status_in_user_id_in_db(self, user_id, new_user_time):
        db = DataBase()
        db.update_last_online_time(user_id, new_user_time)

    # work with bd table user_fingerprint
    def get_time_in_user_fingerprint_from_db(self, user_fingerprint):
        db = DataBase()
        time = db.get_last_time_from_fingerprint(user_fingerprint)[0][1]
        return time

    def update_status_in_user_fingerprint_in_db(self, user_fingerprint,
                                                         new_user_time):
        db = DataBase()
        db.update_last_online_time_in_fingerprint(user_fingerprint, new_user_time)

    # processing requests to storage

    def get_status_from_user_id(self, user_id):
        user_time = self.get_time_from_redis(user_id)
        if not user_time:
            user_time = self.get_time_in_user_id_from_db(user_id)
            self.add_user_to_redis(user_id, user_time)
        return self.check_status(user_time)
        # rows[0][1].strftime("%d-%b-%Y %H:%M:%S.%f")

    def get_status_from_fingerprint(self, string_for_hash):
        user_fingerprint = sha256(string_for_hash.encode('utf-8')).hexdigest()
        user_time = self.get_time_from_redis(user_fingerprint)
        if not user_time:
            user_time = self.get_time_in_user_fingerprint_from_db(
                user_fingerprint)
            self.add_user_to_redis(user_fingerprint, user_time)
        return self.check_status(user_time)

    def update_status_in_user_id(self, user_id, new_user_time):
        self.update_status_in_user_id_in_db(user_id, new_user_time)
        self.add_user_to_redis(user_id, new_user_time)
        return self.status_online

    def update_status_in_fingerprint(self, string_for_hash, new_user_time):
        user_fingerprint = sha256(string_for_hash.encode('utf-8')).hexdigest()
        self.update_status_in_user_fingerprint_in_db(user_fingerprint, new_user_time)
        self.add_user_to_redis(user_fingerprint, new_user_time)
        return self.status_online
