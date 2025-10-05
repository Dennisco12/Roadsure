#!/usr/bin/python3

from models.base_model import BaseModel
from models import storage

class Device(BaseModel):
    __tablename__ = 'devices'
    _vehicle_id: str

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
