from flask import Flask, request
from storage import data_store
from datetime import datetime

app = Flask(__name__)


@app.route('/fingerprint/get_last_online_time/<user_id>', methods=['GET'])
def get_last_online_time_from_storage(user_id=None):
    return data_store("get_lot", user_id)


@app.route('/fingerprint/update_last_online_time/<user_id>', methods=['PUT'])
def update_last_online_time_in_storage(user_id=None):
    values = [request.form[k] for k in request.form]
    return data_store("update_lot", user_id, values[0])


@app.route('/fingerprint/get_last_online_time', methods=['GET'])
def get_last_online_time_for_fingerprint_user():
    string_for_hash = request.remote_addr + request.headers.get('User-Agent')
    current_datetime = datetime.now()
    return data_store("update_tffpu", string_for_hash, current_datetime)

