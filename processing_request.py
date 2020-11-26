from flask import Flask, request
from datetime import datetime

from storage import Storage

app = Flask(__name__)

storage_for_script = Storage()


@app.route('/fingerprint/get_status/<user_id>', methods=['GET'])
def get_last_online_time(user_id=None):
    return storage_for_script.get_status_from_user_id(user_id)


@app.route('/fingerprint/update_status/<user_id>', methods=['GET'])
def update_last_online_time(user_id=None):
    new_user_time = datetime.now()
    return storage_for_script.update_status_in_user_id(user_id, new_user_time)


@app.route('/fingerprint/get_status', methods=['GET'])
def get_last_online_time_for_fingerprint_user():
    string_for_hash = request.remote_addr + request.headers.get('User-Agent')
    return storage_for_script.get_status_from_fingerprint(string_for_hash)


@app.route('/fingerprint/update_status', methods=['GET'])
def update_last_online_time(user_id=None):
    string_for_hash = request.remote_addr + request.headers.get('User-Agent')
    new_user_time = datetime.now()
    return storage_for_script.update_status_in_fingerprint(string_for_hash, new_user_time)


"""
@app.route('/fingerprint/update_last_online_time/<user_id>', methods=['PUT'])
def update_last_online_time(user_id=None):
    values = [request.form[k] for k in request.form]
    return data_store("update_status_in_user_id", user_id, values[0])
"""
