from datetime import datetime
from document_manager.common.database import Database
import uuid


class Document(object):
    def __init__(self, title, content, author, author_id, type="public", created_date=None, id=None):
        self.title = title
        self.content = content
        self.author = author
        self.type = type
        self.created_date = datetime.utcnow() if created_date is None else created_date
        self.author_id = author_id
        self._id = uuid.uuid4().hex if id is None else id

    def json_data(self):
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "type": self.type,
            "created_date": self.created_date,
            "author_id": self.author_id,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(collection='document', data=self.json_data())

    @staticmethod
    def find():
        return [user for user in Database.find(collection="document")]

    @staticmethod
    def find_one_id(id):
        return Database.find_one(collection="document", query={"_id": id})

    @staticmethod
    def find_one_title(title):
        return Database.find_one(collection="document", query={"title": title})

    @staticmethod
    def update(query, data):
        Database.update_one(collection="document", query=query, data={'$inc': data})

    @staticmethod
    def delete(id):
        Database.delete(collection="document", query={"_id": id})
