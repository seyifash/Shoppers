from models.base_model import BaseModel, Base
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class User(BaseModel, Base, UserMixin):
    """creates a new user"""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phoneNumber = Column(String(128), nullable=False)
    orders = relationship('Order', backref='users')
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)