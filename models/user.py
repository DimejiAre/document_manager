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
    def find():
        return [user for user in Database.find(collection="user")]

    @staticmethod
    def find_one_id(id):
        return Database.find_one(collection="user", query={"_id": id})

    @staticmethod
    def find_one_username(username):
        return Database.find_one(collection="user", query={"username": username})

    @staticmethod
    def update_one(query, data):
        Database.update_one(collection="user", query=query, data={'$inc': data})

    @staticmethod
    def delete(id):
        Database.delete(collection="user", query={"_id": id})

