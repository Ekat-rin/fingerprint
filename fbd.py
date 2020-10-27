from flask import Flask

import psycopg2


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(database="fingerprint_database",
                                     user="fingerprint_user",
                                     password="qwerty", host="localhost",
                                     port=5432)
        print("Database opened successfully")
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

    def __del__(self):
        self.cur.close()
        self.conn.close()


# func for work with diffrient data store

def data_store(request, data):
    if request == "get_lot":
        db = DataBase()
        rows = db.get_last_time_from_last_online_time(data)
        return rows[0][1].strftime("%d-%b-%Y %H:%M:%S.%f")

app = Flask(__name__)


@app.route('/fingerprint/get_last_online_time/<user_id>', methods=['GET'])
def get_last_online_time_from_storge(user_id=None):
    return data_store("get_lot", user_id)


if __name__ == '__main__':
   app.run(debug=True)
   #BD = DataBase()
   #rows = BD.get_last_time_from_last_online_time("2355_10")
   #print(rows[0][1].strftime("%d-%b-%Y %H:%M:%S.%f"))
