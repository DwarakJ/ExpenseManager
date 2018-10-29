import threading
from flask_sqlalchemy import SQLAlchemy

#// "postgres://rohjxttodkhhub:7f90930264f10f396dbb652d5879064a66c33fd656a222586186211a596d00a9@ec2-174-129-33-230.compute-1.amazonaws.com:5432/dac80pil4pesjn"
# creating a lock
lock = threading.Lock()

db = SQLAlchemy()

def connect_to_db(app, database):
    """ Connect the database to our Flask app. """

    # Configure to use the database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)

def transaction(data, type):
    lock.acquire()
    try:
        if type == "Add":
            db.session.add(data)
        elif type == "Delete":
            db.session.delete(data)
    finally:
        db.session.commit()
        lock.release()