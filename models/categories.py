from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship

class Category(BaseModel, Base):
    """creates a new product"""
    __tablename__ = 'category'
    name = Column(String(255), nullable=False)
    products = relationship('Product', backref='category')