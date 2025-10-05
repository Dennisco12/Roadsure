#!/usr/bin/python3

import bcrypt
from models import storage
from models.user import User
import random
from api.blueprint import app_views, auth
from flask import jsonify, request
# from api.blueprint.mailer.controller import runner
from settings.token_manager import Manager
# from settings.loadenv import handleEnv

manager = Manager()

def generate_otp():
    return f"{random.randint(100000, 999999)}"


@app_views.route('/users', strict_slashes=False)
def all_users():
    return jsonify([user.to_dict() for _, user in storage.all('User').items()])

@app_views.route('/user', strict_slashes=False, methods=['POST'])
def create_users():
    """This creates a new user in storage"""
    if not request.json:
        return jsonify('Not a valid json'), 400
    user_data = request.get_json()

    if "email" not in user_data:
        return jsonify("Please include an email"), 400
    db_emails = storage.search("User", email=user_data["email"])
    if len(db_emails) > 0:
        return jsonify("Email already exists"), 400
    
    for key, val in user_data.items():
        if key == 'password':
            val = val.encode()
            val = bcrypt.hashpw(val, bcrypt.gensalt())
            user_data[key] = val
        else:
            user_data[key] = val.strip()

    try:
        user = User(**user_data)
        user.save()
    except Exception as e:
        return jsonify(f'Unable to create profile: {str(e)}'), 400
    
    return jsonify(user.to_dict()), 201

@app_views.route('/user/<user_id>', strict_slashes=False, methods=['PUT', 'DELETE', 'GET'])
def get_update_delete_user(user_id):
    """This updates user data in storage"""
    if not request.json:
        return jsonify('Not a valid json'), 400
    
    user: User = storage.get("User", user_id)
    if not user:
        return jsonify("User not found"), 404
    
    if request.method == "PUT":
        user_data = request.get_json()

        for key, val in user_data.items():
            setattr(user, key, val)
            user.save()
            return jsonify(user.to_dict())
    elif request.method == "DELETE":
        storage.delete(user)
        return jsonify({}), 201
    elif request.method == 'GET':
        return jsonify(user.to_dict()), 200

@app_views.route('/user/login', strict_slashes=False, methods=['POST'])
def user_login():
    if not request.json:
        return jsonify('Invalid request'), 400
    passwd = request.get_json().get('password', None)
    email = request.get_json().get('email', None)
    if not passwd or not email:
        return jsonify('Request must include a password and email'), 400
    password = passwd.strip()
    password = password.encode()

    db_user = storage.search('User', email=email.lower())[0]
    try:
        admin_pass = db_user.password.encode()
    except:
        admin_pass = db_user.password

    if bcrypt.checkpw(password, admin_pass):
        token = manager.create_session(db_user.id)
        return jsonify({'token': token, 'message': "Login successful"})
    else:
        return jsonify('Password is incorrect'), 404

@app_views.route('/user/<token>/logout', strict_slashes=False)
@auth.login_required
def user_logout(token):
    user = storage.search('UserSession', token=token)

    if user:
        manager.delete_token(user[0].id)
        return jsonify('user has been logged out')
    else:
        return jsonify('user not found'), 404

# @app_views.route('/request_admin_otp', strict_slashes=False)
# def request_admin_otp():
#     """This sends a mail to the admin for password reset"""
#     # otp = generate_otp()
#     # try:
#     #     runner.sendAdminResetOTP(otp)
#     # except Exception as e:
#     #     return jsonify(f"Error: {e}"), 404
    
#     admin = list(storage.all('Admin').values())
#     if admin:
#         admin = admin[0]
#     else:
#         return jsonify('No admin account found'), 404
    
#     # setattr(admin, 'reset_otp', otp)
#     admin.save()
#     return jsonify('Please check your admin mail for an OTP')

# @app_views.route('/reset_passwd', strict_slashes=False, methods=['POST'])
# def reset_admin_passwd():
#     if not request.json:
#         return jsonify("Not a valid json"), 400
    
#     data = request.get_json()
#     passwd = data.get('password')
#     otp = int(data.get('otp'))

#     admin = list(storage.all('Admin').values())
#     if not admin:
#         return jsonify('No admin account found'), 404
#     else:
#         admin = admin[0]

#     if int(admin.reset_otp) != otp:
#         print(int(admin.reset_otp))
#         print(otp)
#         return jsonify("Incorrect OTP entered"), 400
    
#     passwd = passwd.encode()
#     passwd = bcrypt.hashpw(passwd, bcrypt.gensalt())
#     setattr(admin, 'password', passwd)
#     admin.save()
#     return jsonify("Password reset was successful")
    

