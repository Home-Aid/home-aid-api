from pydantic import BaseModel, validator
from typing import Optional
import re

class Address(BaseModel):
    longitude: float
    latitude: float
    address: str
    city: str
    state: str
    zip: str

    # Validate the zip code
    @validator('zip')
    def zip_validator(cls, zip):
        if not re.match(r"^\d{6}$", zip):
            raise ValueError("Invalid zip code format")
        return zip

class CreateEmployee(BaseModel):
    name: str
    email: str
    hashedPassword: str
    mobile: str
    address: Address
    

    # Validate the email
    @validator('email')
    def email_validator(cls, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    # Validate the mobile number
    @validator('mobile')
    def mobile_validator(cls, mobile):
        if not re.match(r"^[6-9]\d{9}$", mobile):
            raise ValueError("Invalid mobile number format")
        return mobile
    