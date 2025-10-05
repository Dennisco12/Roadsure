#!/usr/bin/python3

from flask import Blueprint
from models import storage
from flask_httpauth import HTTPTokenAuth
from settings.token_manager import Manager

app_views = Blueprint('app_views', __name__, url_prefix='/roadsure')
auth = HTTPTokenAuth(scheme='Roadsure')
manager = Manager()

@auth.verify_token
def verify_token(token):
    """This validates the token presented by the user"""
    if not token:
        return None
    user_id = manager.get_user(token)
    if user_id is None:
        print("No user found")
        manager.delete_token(user_id)
        return None
    user = storage.get('Admin', user_id)
    return user


from api.blueprint.devices import *
from api.blueprint.users import *
from api.blueprint.vehicles import *
from api.blueprint.devices import *
