from document_manager.models.user import User
from document_manager.models.document import Document
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'


# def auth_required(function):
#     @wraps(function)
#     def decorated(*args, **kwargs):
#         function(*args, **kwargs)
#     return decorated


@app.route("/")
def hello():
    if request.authorization and request.authorization.username == 'username1':
        return jsonify({"message": "Hello World!"})

    return make_response("Could not verify!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/login", methods=["POST"])
def login():
    r = request.json
    user = User.find_one_username(r['username'])
    user['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=50)
    if check_password_hash(user['password'], r['password']):
        token = jwt.encode(user, app.config['SECRET_KEY'], )
        return jsonify({"token": token.decode('UTF-8')})
    else:
        return jsonify({"message": "login failed"})


@app.route("/user", methods=["GET"])
def get_users():
    users = User.find()
    if users:
        return jsonify({"users": users})
    else:
        return jsonify({"message": "No users to display"})


@app.route("/user/<id>", methods=["GET"])
def get_one_user_by_id(id):
    user = User.find_one_id(id)
    if user:
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
    user = User(username=r['username'], password=generate_password_hash(r['password'], 'sha1'))
    user.save_to_mongo()
    return jsonify({"message": "{} has been created".format(user.username)})


@app.route("/user/<id>", methods=['PUT'])
def update_user(id):
    r = request.json
    user = User.find_one_class_id(id)
    print(user.username)
    print(type(r))
    print(r)
    if user:
        user.update_one(r)
        return jsonify({"message": "{} has been updated".format(user.username)})
    else:
        return jsonify({"message": "User not found"})


@app.route("/user/<id>", methods=['DELETE'])
def delete_user(id):
    user = User.find_one_class_id(id)
    if user:
        user.delete()
        return jsonify({"message": "{} has been deleted".format(user.username)})
    else:
        return jsonify({"message": "User not found"})


@app.route("/document", methods=["GET"])
def get_documents():
    docs = Document.find()
    if docs:
        return jsonify({"documents": docs})
    else:
        return jsonify({"message": "No documents found"})


@app.route("/<id>/document", methods=["GET"])
def get_documents_by_author(id):
    docs = Document.find_by_author(id)
    if docs:
        return jsonify({"documents": docs})
    else:
        return jsonify({"message": "No documents found"})


@app.route("/document/<id>", methods=["GET"])
def get_one_document_by_id(id):
    doc = Document.find_one_id(id)
    if doc:
        return jsonify(doc)
    else:
        return jsonify({"message": "Document does not exist"})


# user_id to be gotten from logged in user
@app.route("/document", methods=['POST'])
def post_document():
    user_id = "11111"
    r = request.json
    document = Document(title=r["title"], content=r["content"], author=r["author"], author_id=user_id)
    document.save_to_mongo()
    return jsonify({"message": "Document has been successfully created"})


@app.route("/document/<id>", methods=['PUT'])
def update_document(id):
    r = request.json
    document = Document.find_one_class_id(id)
    if document:
        document.update(r)
        return jsonify({"message": "Document has been updated"})
    else:
        return jsonify({"message": "Document does not exist"})


@app.route("/document/<id>", methods=['DELETE'])
def delete_document(id):
    document = Document.find_one_class_id(id)
    if document:
        document.delete()
        return jsonify({"message": "Document has been deleted"})
    else:
        return jsonify({"message": "Document does not exist"})


if __name__ == '__main__':
    app.run(debug=True, port=4000)










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
