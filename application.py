import os
import datetime
import sys
import json
from flask import Flask, request, Response, jsonify, session
from models.spend import Spend, User
from service.databaseservice import transaction, connect_to_db
from service.authentication import Register, Login, Logout, validation
from functools import wraps

app = Flask(__name__)

# Getting configs
with open(os.path.join(sys.path[0], "project_config.json"), "r") as f:
    general_config = json.load(f)

# Connect to database
connect_to_db(app, general_config["database_url"])

# Adding secret key for session
app.config['SECRET_KEY'] = os.urandom(24)
app.secret_key = os.environ["APP_SECRET_KEY"]

@app.route("/", methods=["GET"])
def expense_list():
    expenses = Spend.query.filter_by(Spend.user_id == getUserId()).order_by(Spend.date.desc()).all()
    return jsonify(Spend.serialize_list(expenses))

@app.route("/expense", methods=["POST"])
def create():
    req_data = request.get_json()
    expense = Spend(
        item=req_data["item"],
        amount=float(req_data["amount"]),
        paid_to=req_data["paid_to"],
        category=req_data["category"],
        date=datetime.datetime.now(),
        description=req_data["description"]
    )
    transaction(expense, "Add")
    return Response("Added Successfully")

@app.route("/expense/<int:id>")
def detail(id):
    expense = Spend.query.get(id)
    if not expense:
        return Response("Not found")
    return jsonify(expense.serialize())

@app.route("/expense/<int:id>/edit", methods=["POST"])
def edit(id):
    expense = Spend.query.get(id)
    if not expense:
        return Response("Not found")

    req_data = request.get_json()

    expense.item = req_data["item"]
    expense.amount = float(req_data["amount"])
    expense.paid_to = req_data["paid_to"]
    expense.category = req_data["category"]
    expense.description = req_data["description"]
    transaction(expense, "Add")
    return Response("Edited Successfully")

@app.route("/expense/<int:id>/delete", methods=["DELETE"])
def delete(id):
    expense = Spend.query.get(id)
    if expense:
        transaction(expense, "Delete")
    return Response("Deleted Successfully")

@app.route("/expense/<string:category>", methods=["GET", "POST"])
def category(category):
    expenses = Spend.query.filter(Spend.category == category).order_by(Spend.date.desc()).all()
    return jsonify(Spend.serialize_list(expenses))

@app.route("/register", methods=["POST"])
def create_user():
    req_data = request.get_json()
    user = User(
        name=req_data["name"],
        email=req_data["email"],
        password=req_data["password"],
        create_date=datetime.datetime.now()
    )

    if Register(user):
        return Response("Added Successfully")
    else:
        return Response("Registration Failed !!! User already exist")


@app.route("/login", methods=["POST"])
def login():
    req_data = request.get_json()
    if Login(req_data["username"], req_data["password"]):
        session['logged_in'] = True
        session['username'] = req_data["username"]
        current_user = session['username']
        return Response("Login Successful! Welcome "+ session['username'])
    else:
        return Response("Login Failed!!! Check username and password")

@app.route("/logout", methods=['GET'])
def logout():
    session.clear()

def getUserId():
    username = session['username']
    return User.query.filter(User.name == username).first().id

if __name__ == "__main__":
    current_user= ""
    app.run()