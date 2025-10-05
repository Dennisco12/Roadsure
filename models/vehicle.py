#!/usr/bin/python3

from models.base_model import BaseModel


class Vehicle(BaseModel):
    __tablename__ = 'vehicles'

    _user_id: str
    _device_id: str
    reg_no: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, str):
            raise TypeError("User id must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Please enter a valid user id")
        self._user_id = value

    @property
    def device_id(self):
        return self._device_id
    
    @device_id.setter
    def device_id(self, value):
        if not isinstance(value, str):
            raise TypeError("Device id must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Please enter a valid device_id")
        self._device_id = value