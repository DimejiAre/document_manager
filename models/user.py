import uuid
from document_manager.common.database import Database


class user(object):
    def __init__(self, username, password, role, _id=None):
        self.username = username
        self.password = password
        self.role = role  # user(r), admin(w,r)
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_json(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(collection='user', data=self.get_json())

    @staticmethod
    def find_one_id(id):
        pass

    @staticmethod
    def find_one_username(name):
        pass

    def update_one(self):
        pass

    @staticmethod
    def delete(id):
        pass

