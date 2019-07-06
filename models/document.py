from datetime import datetime
from document_manager.common.database import Database
import uuid


class Document(object):
    def __init__(self, title, content, author, author_id, type="public", created_date=None, _id=None):
        self.title = title
        self.content = content
        self.author = author
        self.type = type
        self.created_date = datetime.utcnow() if created_date is None else created_date
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

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
        return [doc for doc in Database.find(collection="document")]

    @staticmethod
    def find_one_id(id):
        return Database.find_one(collection="document", query={"_id": id})

    @classmethod
    def find_one_class_id(cls,id):
        doc_data = Database.find_one(collection="document", query={"_id": id})
        return cls(**doc_data)

    @staticmethod
    def find_one_title(title):
        return Database.find_one(collection="document", query={"title": title})

    def update(self, data):
        Database.update_one(collection="document", query={"_id": self._id}, data={'$set': data})

    def delete(self):
        Database.delete(collection="document", query={"_id": self._id})
