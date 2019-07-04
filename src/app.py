from document_manager.models.user import User
from document_manager.models.document import Document
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/user", methods=["GET"])
def get_users():
    users = User.find()
    if users is not None:
        return jsonify({"users": users})
    else:
        return jsonify({"message": "No users to display"})


@app.route("/user/<id>", methods=["GET"])
def get_one_user_by_id(id):
    user = User.find_one_id(id)
    if user is not None:
        return jsonify(user)
    else:
        return jsonify({"message": "User does not exist"})


# @app.route("/user/<username>", methods=["GET"])
# def get_one_user_by_username(username):
#     user = User.find_one_username(username)
#     if user is not None:
#         return jsonify(user)
#     else:
#         return jsonify({"message": "User does not exist"})


@app.route("/user", methods=['POST'])
def post_user():
    r = request.json
    user = User(username=r['username'], password=r['password'])
    user.save_to_mongo()
    return jsonify({"message": "{} has been created".format(user.username)})

# Update_user not yet working
@app.route("/user/<id>", methods=['PUT'])
def update_user(id):
    r = request.json
    user = User.find_one_class_id(id)
    if user is not None:
        user.update_one(r)
        return jsonify({"message": "{} has been updated".format(user.username)})
    else:
        return jsonify({"message": "User not found"})


@app.route("/user/<id>", methods=['DELETE'])
def delete_user(id):
    user = User.find_one_class_id(id)
    if user is not None:
        user.delete()
        return jsonify({"message": "{} has been deleted".format(user.username)})
    else:
        return jsonify({"message": "User not found"})


@app.route("/document", methods=["GET"])
def get_documents():
    return jsonify([doc for doc in Document.find()])


if __name__ == '__main__':
    app.run(debug=True)










    # from document_manager.common.database import Database
    #
    #
    # def test_insert(collection, data):
    #     Database.insert(collection, data)
    #
    #
    # def test_find(collection):
    #     print([user for user in Database.find(collection)])
    #
    #
    # def test_find_one(collection, query=None):
    #     print(Database.find_one(collection, query={"age": 47}))
    #
    # def test_update():
    #         print(Database.update_one(collection="user", query={"name": "damola"}, data={'$inc': {'age': 32}}))
    #
    # def test_delete():
    #     Database.delete("user", {"age": 47})
    #
    #
    # collection = 'user'
    # data = {
    #     "name": "Sorinmade",
    #     "age": 47
    # }
    #
    # # test_insert(collection,data)
    #
    # # test_find_one("user")
    #
    # test_update()
