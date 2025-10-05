#!/usr/bin/python3


from models.base_model import BaseModel


class UserSession(BaseModel):
    __tablename__ = 'usersession'

    def __init__(self, *args, **kwargs):
        if "token" not in kwargs:
            raise ValueError("Token parameter missing")
        if "user_id" not in kwargs:
            raise ValueError("User id parameter missing")
        
        super().__init__(*args, **kwargs)

        for key, val in kwargs.items():
            if key != '__class__':
                setattr(self, key, val)
