#!usr/bin/python3

from datetime import datetime, timedelta
import uuid
from models.user_session import UserSession
from models import storage

time = "%b %d %Y, %I:%M:%S %p"


def generate_id() -> str:
    """This generates a unique id every time it is called"""
    token = str(uuid.uuid4())
    return token


class Manager():
    """this handles token creation and expiration"""
    _duration = 24 * 60 * 60    # 24 hours

    def create_session(self, user_id:str=None)-> str:
        """This generates a token and stores it for the user"""
        # search for any existing session and delete them
        sessions = storage.search("UserSession", user_id=user_id)
        if sessions:
            for session in sessions:
                session.delete()
                
        token = generate_id()
        token_dict = {
            'token': token,
            'user_id': user_id
        }
        model = UserSession(**token_dict)
        model.save()
        return token

    def get_user(self, token:str=None):
        """This retrieves a user based on the given token"""
        if token is None:
            return None
        sess = storage.search('UserSession', token=token)
        if sess is None or len(sess) == 0:
            return None
        created_at = sess[0].created_at
        try:
            if isinstance(created_at, str):
                created_at = datetime.strptime(created_at, time)
            valid_period = created_at + timedelta(seconds = self._duration)
            if valid_period < datetime.now():
                self.delete_token(sess[0].user_id)
                return None
            return sess[0].user_id
        except Exception as e:
            print(created_at)
            print(str(e))
            # print(type(timedelta(seconds = self._duration)))
        
    def delete_token(self, user_id:str):
        """This deletes a user session token"""
        obj = storage.search('UserSession', user_id=user_id)
        if obj != [] and obj is not None:
            storage.delete(obj[0])
