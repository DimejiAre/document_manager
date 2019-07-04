from document_manager.common.database import Database


def test_insert(collection, data):
    Database.insert(collection, data)


def test_find(collection):
    print([user for user in Database.find(collection)])


def test_find_one(collection, query=None):
    print(Database.find_one(collection, query={"age": 47}))

def test_update():
        print(Database.update_one(collection="user", query={"name": "damola"}, data={'$inc': {'age': 32}}))

def test_delete():
    Database.delete("user", {"age": 47})


collection = 'user'
data = {
    "name": "Sorinmade",
    "age": 47
}

# test_insert(collection,data)

# test_find_one("user")

test_update()