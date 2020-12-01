import psycopg2
import json


# "database_config_user_last_time.json"
# "database_config_fingerprint.json.json"

class DataBase:
    def __init__(self, config):
        with open(config, "r") as read_file:
            database_conf = json.load(read_file)
        self.conn = psycopg2.connect(database=database_conf["database"],
                                     user=database_conf["user"],
                                     password=database_conf["password"],
                                     host=database_conf["host"],
                                     port=database_conf["port"])
        self.cur = self.conn.cursor()
        self.table = database_conf["table"]

    def get(self, user_id):
        if self.table is "user_last_online":
            self.cur.execute(
                f"SELECT user_id, last_online_time "
                f"FROM {self.table}"
                f"WHERE user_id = {user_id}")
        if self.table is "user_fingerprint":
            self.cur.execute(
                f"SELECT user_id, fingerprint"
                f"FROM {self.table}"
                f"WHERE fingerprint = {user_id}")
        result = self.cur.fetchall()
        return result[0]

    def update(self, user_id=None, new_data=None):
        if self.table is "user_last_online":
            self.cur.execute(
                f"UPDATE user_last_online "
                f"set last_online_time = {new_data}"
                f"where user_id = {user_id}")

        if self.table is "user_fingerprint":
            self.cur.execute(
                f"INSERT INTO user_fingerprint (fingerprint)"
                f"VALUES ({new_data})")
        self.conn.commit()
        return True

    def __del__(self):
        self.cur.close()
        self.conn.close()
