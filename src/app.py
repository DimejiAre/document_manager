from document_manager.common.database import Database


def test_insert(collection, data):
    Database.insert(collection, data)


def test_find(collection):
    print(Database.find(collection))


collection = 'user'
data = {
    "name": "dimeji",
    "age": 27
}

test_insert(collection,data)

test_find(collection)
