from pymongo import MongoClient


class Database(object):
    client = MongoClient()
    db = client['DM']

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert(data)

    @staticmethod
    def find(collection):
        return Database.db[collection].find_one()
