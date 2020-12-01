import redis


class redis_storage:
    def __init__(self):
        self.red = redis.Redis()

    # work with cash
    def get(self, user_id):
        return [user_id, self.red.get(user_id)]

    def update(self, user_id, new_data):
        self.red.set(user_id, new_data)
        return True
