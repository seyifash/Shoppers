from models.base_model import BaseModel, Base
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy import String, Column, Boolean, DateTime
from sqlalchemy.orm import relationship


class Seller(BaseModel, Base, UserMixin):
    """creates a new seller"""
    __tablename__ = 'seller'
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    is_confirmed = Column(Boolean, default=False)
    confirmed_at = Column(DateTime, nullable=True)
    
    products = relationship('Product', backref='seller')
    orders = relationship('Order', backref='seller')
    
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
        
    def confirm_email(self):
        self.is_confirmed = True
        self.confirmed_at = datetime.utcnow()