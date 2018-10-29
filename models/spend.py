from service.databaseservice import db
from service.serializer import Serializer

class Spend(db.Model, Serializer):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Unicode)
    amount = db.Column(db.Float)
    paid_to = db.Column(db.Unicode)
    category = db.Column(db.Unicode)
    date = db.Column(db.Date)
    description = db.Column(db.Unicode)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref=db.backref('expenses'))

class Revenue(db.Model, Serializer):
    __tablename__ = "revenue"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    category = db.Column(db.Unicode)
    date = db.Column(db.Date)
    description = db.Column(db.Unicode)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref=db.backref('revenue'))

class User(db.Model, Serializer):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    password = db.Column(db.Unicode)
    create_date = db.Column(db.Date)

class Budget(db.Model, Serializer):
    __tablename__ = "budget"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    budget_amount = db.Column(db.Float)
    budget_userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    budget_month = db.Column(db.Integer)
    budget_year = db.Column(db.Integer)

    user = db.relationship("User", backref=db.backref('budget'))