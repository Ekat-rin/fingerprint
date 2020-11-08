from database import DataBase
from hashlib import sha256


# func for work with diffrient data store
def data_store(request, data_get=None, data_put=None):
    if request == "get_lot":
        db = DataBase()
        rows = db.get_last_time_from_last_online_time(data_get)
        return rows[0][1].strftime("%d-%b-%Y %H:%M:%S.%f")

    if request == "update_lot":
        db = DataBase()
        db.update_last_online_time(data_get, data_put)
        return "updated"

    if request == "update_tffpu":
        hashed_word = sha256(data_get.encode('utf-8')).hexdigest()
        db = DataBase()
        db.update_last_online_time(hashed_word, '{:%Y-%m-%d %H:%M:%S}'.
                                   format(data_put))
        return "use finger_print"
