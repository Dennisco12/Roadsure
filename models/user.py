#!/usr/bin/python3

from models.base_model import BaseModel
from typing import List


class User(BaseModel):
    __tablename__ = "users"
    _first_name: str
    _last_name: str
    _company_name: str
    _phone_number: str
    _email: str
    _is_corporate: bool = False
    vehicles_id: List

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_corporate = False

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if self._is_corporate is True:
            raise TypeError("Corporate users can only have company name")
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        value = value.strip()
        if not value:
            raise TypeError("Please enter a valid last name")
            
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if self._is_corporate is True:
            raise TypeError("Corporate users can only have company name")
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        value = value.strip()
        if not value:
            raise TypeError("Please enter a valid last name")
            
        self._first_name = value
    
    @property
    def company_name(self):
        return self._company_name
    
    @company_name.setter
    def company_name(self, value):
        if self._is_corporate is False:
            raise AttributeError("Only corporate accounts can have company name")
        if not isinstance(value, str):
            raise TypeError("company name must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Please enter a valid company name")
        self._company_name = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value:
            raise ValueError("Please add an email")
        
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        value = value.strip()
        
        if "@" not in value or ".com" not in value.lower():
            raise ValueError("Invalid email entered")
        
        setattr(self, "_email", value.lower())

    @property
    def phone_no(self):
        return self._phone_no
    
    @phone_no.setter
    def phone_no(self, value):
        if not isinstance(value, str):
            raise TypeError("phone_no must be a str")
        if value[0] == "+":
            value = value[1:]
        if not value.isdigit():
            raise ValueError("phone_no must be a number")
        value = str(value)
        if value.startswith("234") and len(value) == 13:
            value = "0" + value[3:]
        elif value.startswith("0"):
            value = value
        else:
            value = "0" + value

        if len(value) != 11 and len(value) != 14:
            raise ValueError(f"phone_no must contain 11 digits: {value}")
        self._phone_no = value

    @property
    def is_corporate(self):
        return self._is_corporate
    
    @is_corporate.setter
    def is_corporate(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_corporate value must be boolean")
        self._is_corporate = value

if __name__ == '__main__':
    usr = User()
    print(usr.to_dict())
