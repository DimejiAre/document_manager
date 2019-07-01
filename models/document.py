from datetime import datetime
from document_manager.common.database import Database
import uuid


class Document(object):
    def __init__(self, title, content, author, created_date=None, id=None):
        self.title = title
        self.content = content
        self.author = author
        self.created_date = datetime.utcnow() if created_date is None else created_date
        self._id = uuid.uuid4().hex if id is None else id

    def json_data(self):
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_date": self.created_date,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(collection='document', data=self.json_data())

    @staticmethod
    def find_one_id(id):
        pass

    @staticmethod
    def find_one_title(title):
        pass

    def update(self):
        pass

    @staticmethod
    def delete(id):
        pass
