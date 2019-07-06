import uuid
from document_manager.common.database import Database


class User(object):
    def __init__(self, username, password, admin=False, _id=None):
        self.username = username
        self.password = password
        self.admin = admin  # user(r), admin(w,r)
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_json(self):
        return {
            "username": self.username,
            "password": self.password,
            "admin": self.admin,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(collection='user', data=self.get_json())

    @staticmethod
    def find():
        return [user for user in Database.find(collection="user")]

    @staticmethod
    def find_one_id(id):
        return Database.find_one(collection="user", query={"_id": id})

    @classmethod
    def find_one_class_id(cls,id):
        user_data = Database.find_one(collection="user", query={"_id": id})
        return cls(**user_data)

    @staticmethod
    def find_one_username(username):
        return Database.find_one(collection="user", query={"username": username})

    @classmethod
    def find_one_class_username(cls, username):
        user_data = Database.find_one(collection="user", query={"username": username})
        return cls(**user_data)

    def update_one(self, data):
        Database.update_one(collection="user", query={"_id": self._id}, data={'$set': data})

    def delete(self):
        Database.delete(collection="user", query={"_id": self._id})

