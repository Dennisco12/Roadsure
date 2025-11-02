#!/usr/bin/python3

from models.base_model import BaseModel
from models import storage

class Device(BaseModel):
    __tablename__ = 'devices'
    _vehicle_id: str
    _owner_id: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def vehicle_id(self):
        return self._vehicle_id
    
    @vehicle_id.setter
    def vehicle_id(self, value):
        if not isinstance(value, str) or not value.strip():
            raise TypeError("vehicle_id must be a valid string")
        
        value = value.strip()
        veh = storage.get("Vehicle", value)
        if not veh:
            raise ValueError("Invalid vehicle id")
        setattr(self, "_vehicle_id", value)

    @property
    def owner_id(self):
        return self._owner_id
    
    @owner_id.setter
    def owner_id(self, value):
        if not isinstance(value, str) or not value.strip():
            raise TypeError("Owner id not be a str")
        
        value = value.strip()
        owner = storage.get("User", value)
        if not owner:
            raise ValueError(f"User with id {value} does not exist")
        setattr(self, "_owner_id", value)
