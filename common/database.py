from pymongo import MongoClient


class Database(object):
    client = MongoClient()
    db = client['DM']

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert_one(data)

    @staticmethod
    def find(collection):
        return Database.db[collection].find()

    @staticmethod
    def find_one(collection, query):
        return Database.db[collection].find_one(query)

    @staticmethod
    def update_one(collection, query, data):
        Database.db[collection].update_one(query,data)

    @staticmethod
    def delete(collection, query):
        Database.db[collection].delete_one(query)
