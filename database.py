import os
import random
import sys
import json
import datetime
from flask import Flask
from service.databaseservice import db, connect_to_db
from models.spend import Spend, User, Revenue, Budget
from faker import Faker

fake = Faker()

app = Flask(__name__)

categories = [
    "rent", "utilities", "groceries", "food",
    "diapers", "autoloan", "booze", "therapist"
]

if bool(os.environ.get('DEBUG', '')):
    db.drop_all()

values = range(1, 11)

users = [
    User(
        name= fake.name(),
        email= fake.text(5)+"@gmail.com",
        password= fake.text(10),
        create_date= datetime.datetime.now()
    ) for i in range(10)
]

revenue = [
    Revenue(
        amount=random.random() * random.randint(10, 1000),
        category=random.choice(categories),
        date=fake.date_time_between(start_date="-5y", end_date="now", tzinfo=None),
        description=fake.text(100),
        user_id=random.choice(values)
    ) for i in range(50)
]

expenses = [
    Spend(
        item=fake.company(),
        amount=random.random() * random.randint(10, 1000),
        paid_to=fake.name(),
        category=random.choice(categories),
        date=fake.date_time_between(start_date="-5y", end_date="now", tzinfo=None),
        description=fake.text(100),
        user_id= random.choice(values)
    ) for i in range(100)
]

# Getting configs
with open(os.path.join(sys.path[0], "project_config.json"), "r") as f:
    general_config = json.load(f)

# Connect to database
connect_to_db(app, general_config["database_url"])
db.create_all()
db.session.add_all(users)
db.session.add_all(revenue)
db.session.add_all(expenses)
db.session.commit()
