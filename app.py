from document_manager.models.user import User
from document_manager.models.document import Document
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import Flask, jsonify, request, make_response, render_template, session

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'secretkey'


def auth_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if "token" in request.headers and request.headers["token"]:
            try:
                token = request.headers["token"]
                print(token)
                user_data = jwt.decode(token, app.config['SECRET_KEY'])
                print("user_data", user_data)
                return function(user_data, *args, **kwargs)
            except:
                return jsonify({"message": "Invalid token"})
        else:
            return jsonify({"message": "Token missing"})

    return decorated


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/authorise")
def hello():
    if request.authorization and request.authorization.username == 'username1':
        return jsonify({"message": "Hello World!"})

    return make_response("Could not verify!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/login", methods=['GET', 'POST'])
def login():
    # try, except block
    # if user does not exist
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = User.find_one_username(username)
        docs = Document.find_by_author(user['_id'])
        user['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=50)
        if check_password_hash(user['password'], password):
            token = jwt.encode(user, app.config['SECRET_KEY'])
            session['token'] = token
            return render_template("profile.html", user=user['username'], docs=docs)
        else:
            return render_template("login.html", no_login="Login failed. Check username and apssword")

    return render_template("login.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['token'] = ""
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]
        user = User(name, username, generate_password_hash(password, 'sha1'), email, phone)
        user.save_to_mongo()
        return render_template("register.html", registered="{} has been created".format(name))
    return render_template("register.html")


@app.route("/create_document", methods=['POST', 'GET'])
def create_document():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        type = request.form['type']
        data = jwt.decode(session["token"],key=app.config['SECRET_KEY'])
        document = Document(title,content,data['username'],data['_id'],type)
        document.save_to_mongo()
        return render_template("document.html", saved_document="Document has been created... ish")
    return render_template("document.html")


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
@auth_required
def post_document(user_data):
    user_id = user_data["_id"]
    print(user_id)
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
    app.run(debug=True, port=4200)










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
