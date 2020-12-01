from flask import Flask
from hashlib import sha256

from cachedStorage import CachedStorage
from redis_cash import redis_storage

HOST_PORT="5050"
fingerprint_app = Flask(__name__)

storage_for_script = CachedStorage("database_config_fingerprint.json.json",
                                                      redis_storage())


@fingerprint_app.route('/fingerprint/get_id/<user_string>', methods=['GET'])
def get_id(user_string=None):
    if user_string:
        user_fingerprint = sha256(user_string.encode('utf-8')).hexdigest()
        user_id_for_fingerprint = storage_for_script.get(user_fingerprint)[1]
        if not user_id_for_fingerprint:
            if storage_for_script.update(user_fingerprint, None):
                user_id_for_fingerprint = storage_for_script.get(user_fingerprint)[1]
        return user_id_for_fingerprint
