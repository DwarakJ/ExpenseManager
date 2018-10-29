from flask import session
from models.spend import User
from passlib.hash import sha256_crypt
from service.databaseservice import transaction

def Register(user):
    user.password = sha256_crypt.encrypt(str(user.password))
    if validation(user.name, user.email, user.password):
        transaction(user, "Add")
        return True
    else:
        return False

def Login(username, password):
    #_password = sha256_crypt.encrypt(str(password))
    if verify(username, password):
        return True
    else:
        return False

def Logout():
    return

def DeRegister():
    return

def verify(_username, _password):
    """Check login credentials"""
    if User.query.filter_by(name=_username).first() is None:
        print("No such user found with this username", "warning")
        return False
    if not sha256_crypt.verify(_password, User.query.filter_by(name=_username).first().password):
        print("Invalid Credentials, password isn't correct!", "danger")
        return False

    return True

def validation(_username, _email, _password):
    """Check if the user already exist in the database"""
    if User.query.filter_by(name=_username).first() is not None:
        print('User Already registered with username {}'.format(
            User.query.filter_by(name=_username).first().name), "warning")
        return False

    if User.query.filter_by(email=_email).first() is not None:
        print('Email is already registered with us with username {}'.format(
            User.query.filter_by(email=_email).first().name), "warning")
        return False

    return True