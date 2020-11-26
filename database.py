import psycopg2
import json


class DataBase:
    def __init__(self):
        with open("database_config.json", "r") as read_file:
            database_conf = json.load(read_file)
        self.conn = psycopg2.connect(database=database_conf["database"],
                                     user=database_conf["user"],
                                     password=database_conf["password"],
                                     host=database_conf["host"],
                                     port=database_conf["port"])
        self.cur = self.conn.cursor()

    def get_last_time_from_last_online_time(self, id_user):
        self.cur.execute(
            """SELECT user_id, last_online_time FROM user_last_online 
                        WHERE user_id = '""" + id_user + """'""")
        return self.cur.fetchall()

    def update_last_online_time(self, id_user, new_time):
        self.cur.execute("""UPDATE user_last_online set last_online_time
                                          = '""" + new_time + """' where 
                                      user_id ='""" + id_user + """'""")
        self.conn.commit()

        #добавить работу базы с fingerprint

    def get_last_time_from_fingerprint(self, user_fingerprint):
        self.cur.execute(
            """SELECT user_id, last_online_time FROM fingerprint_last_online 
                        WHERE user_fingerprint = '""" + user_fingerprint + """'""")
        return self.cur.fetchall()

    def update_last_online_time_in_fingerprint(self, user_fingerprint,
                                                         new_user_time):
        self.cur.execute("""UPDATE fingerprint_last_online set last_online_time
                                                  = '""" + user_fingerprint + """' where 
                                              user_fingerprint ='""" + new_user_time + """'""")
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()
