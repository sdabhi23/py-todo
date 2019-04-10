from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import os

app = Flask(__name__)
app.config["DEBUG"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(10))
    token = db.Column(db.String(12))


class Todo(db.Model):

    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(1024))
    message = db.Column(db.String(10240))
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    created_on = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)


def id_generator(size=12, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route("/")
def index():
    return jsonify({"greeting": "Welcome to the PyTODO API. You can find the docs on https://sdabhi23.github.io/py-todo/"})


@app.route("/signup", methods=['POST'])
def signup():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(name=data["name"]).first()
    if(user == None):
        new_user = User(name=data["name"], password=data["password"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"res_code": "200"})
    else:
        return jsonify({"res_code": "403"})


@app.route("/login", methods=['POST'])
def login():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(name=data["name"]).first()
    if user == None:
        return jsonify({"res_code": "403"})
    else:
        if user.password == data["password"]:
            new_token = id_generator()
            user.token = new_token
            db.session.commit()
            return jsonify({"res_code": "200", "token": user.token})
        else:
            return jsonify({"res_code": "403"})


@app.route("/user", methods=['POST'])
def user():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(token=data["token"]).first()
    if user == None:
        return jsonify({"res_code": "403"})
    else:
        return jsonify({"res_code": "200", "name": user.name})


@app.route("/check_token", methods=['POST'])
def check_token():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(name=data["name"]).first()
    if user == None:
        return jsonify({"403": "User does not exist"})
    else:
        if user.token == data["token"]:
            return jsonify({"res_code": "200"})
        else:
            return jsonify({"res_code": "403"})


@app.route("/logout", methods=["POST"])
def logout():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(token=data["token"]).first()
    if user == None:
        return jsonify({"res_code": "403"})
    else:
        user.token = None
        db.session.commit()
        return jsonify({"res_code": "200"})


@app.route("/new_todo", methods=["POST"])
def newTodo():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(token=data["token"]).first()
    if user == None:
        return jsonify({"res_code": "403"})
    else:
        todo = Todo(user_id=user.id,
                    title=data["title"], message=data["message"])
        db.session.add(todo)
        db.session.commit()
        return jsonify({"res_code": "200"})


@app.route("/list_todo", methods=["POST"])
def viewTodo():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(token=data["token"]).first()
    if user == None:
        return jsonify({"res_code": "403"})
    else:
        todos = Todo.query.filter(Todo.user_id == user.id).all()
        data = []
        for todo in todos:
            data.append({"id": todo.id, "title": todo.title, "message": todo.message, "is_completed": todo.is_completed,
                         "created_on": todo.created_on.strftime("%m/%d/%Y, %H:%M:%S"), "updated_on": todo.updated_on.strftime("%m/%d/%Y, %H:%M:%S")})
        return jsonify({"res_code": "200", "todos": data})


@app.route("/toggle_todo", methods=["POST"])
def toggleTodo():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(token=data["token"]).first()
    if user == None:
        return jsonify({"res_code": "403"})
    else:
        todo = Todo.query.filter_by(id=data["todo_id"]).first()
        if todo == None:
            return jsonify({"res_code": "404"})
        else:
            todo.is_completed = not todo.is_completed
            todo.updated_on = datetime.utcnow()
            db.session.commit()
            return jsonify({"res_code": "200"})


@app.route("/delete_todo", methods=["POST"])
def deleteTodo():
    if not request.json:
        abort(400)
    data = request.json
    user = User.query.filter_by(token=data["token"]).first()
    if user == None:
        return jsonify({"res_code": "403"})
    else:
        todo = Todo.query.filter_by(id=data["todo_id"]).first()
        if todo == None:
            return jsonify({"res_code": "404"})
        else:
            db.session.delete(todo)
            db.session.commit()
            return jsonify({"res_code": "200", "deleted": {"id": todo.id, "title": todo.title, "message": todo.message}})
