from flask import Flask, request
from datetime import datetime

from cachedStorage import CachedStorage
from redis_cash import redis_storage
from storage import Storage

import requests

app = Flask(__name__)

storage_for_script = Storage(CachedStorage
                             ("database_config_user_last_time.json",
                              redis_storage()))


@app.route('/fingerprint/get_status/<user_id>', methods=['GET'])
def get_status_for_login_user(user_id=None):
    return storage_for_script.get(user_id)


@app.route('/fingerprint/update_status/<user_id>', methods=['GET'])
def update_last_online_time(user_id=None):
    new_user_time = datetime.now()
    return storage_for_script.update(user_id, new_user_time)


@app.route('/fingerprint/get_status', methods=['GET'])
def get_status_for_fingerprint_user():
    string_for_hash = request.remote_addr + request.headers.get('User-Agent')
    # послать запрос на сервер с фингерпринтом получить id_user
    response = requests.get(
    f"http://localhost:5000/fingerprint//fingerprint/get_id/{string_for_hash}")
    user_id = response
    return storage_for_script.get(user_id)


@app.route('/fingerprint/update_status', methods=['GET'])
def update_last_online_time(user_id=None):
    string_for_hash = request.remote_addr + request.headers.get('User-Agent')
    new_user_time = datetime.now()
    # послать запрос на сервер с фингерпринтом получить id_user
    response = requests.get(
        f"http://localhost:5000/fingerprint//fingerprint/get_id/{string_for_hash}")
    user_id = response
    return storage_for_script.update(user_id, new_user_time)
