#!/usr/bin/python3

import uuid
import models
from datetime import datetime

time = "%b %d %Y, %I:%M:%S %p"


class BaseModel:
    """class definition"""

    def __init__(self, *args, **kwargs):
        """class initialization"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(kwargs.get("created_at", None)) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.now()
            if kwargs.get("updated_at", None) and type(kwargs.get("updated_at", None)) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.now()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def to_dict(self):
        """This returns a dict representation of the object"""
        dictionary = self.__dict__.copy()
        if 'created_at' in dictionary and not isinstance(dictionary['created_at'], str):
            dictionary['created_at'] = self.created_at.strftime(time)
        if 'updated_at' in dictionary and not isinstance(dictionary['updated_at'], str):
            dictionary['updated_at'] = self.updated_at.strftime(time)
        dictionary.pop('_id', None)
        updated_dict = {}
        for key, value in dictionary.items():
            if key[0] == "_":
                updated_dict[key[1:]] = value
            else:
                updated_dict[key] = value
        updated_dict['__class__'] = self.__class__.__name__
        return updated_dict

    def __str__(self):
        """Called when print function is used"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.to_dict())

    def save(self):
        """This save the object to storage"""
        self.updated_at = datetime.now()
        # models.storage.new(self)
        models.storage.save(self)

    def update(self, **kwargs):
        """This updates some attribute in storage"""
        try:
            for key, val in kwargs.items():
                if key == "password":
                    if self.reset_code == "Valid":
                        setattr(self, key, val)
                    else:
                        pass
                else:
                    setattr(self, key, val)
                models.storage.save()
        except Exception:
            pass

    def delete(self):
        """This removes an object from storage"""
        models.storage.delete(self)
        # models.storage.save()
        del self

