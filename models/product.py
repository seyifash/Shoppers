from models.base_model import BaseModel, Base
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy import String, Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """creates a new product"""
    __tablename__ = 'product'
    productName = Column(String(255), nullable=False)
    productPrice = Column(Integer, nullable=False)
    productQuantity = Column(Integer, nullable=False)
    productSize = Column(JSON, nullable=False)
    productTotal = Column(Integer, nullable=False)
    productDescription = Column(Text, nullable=False)
    seller_id = Column(String(60), ForeignKey('seller.id'), nullable=False)
    category_id = Column(String(60), ForeignKey('category.id'), nullable=False)