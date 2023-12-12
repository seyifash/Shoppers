from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Order(BaseModel, Base):
    """creates a new product"""
    __tablename__ = 'order'
    productName = Column(String(255), nullable=False)
    productPrice = Column(Integer, nullable=False)
    productQuantity = Column(Integer, nullable=False)
    productTotal = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    seller_id = Column(String(60), ForeignKey('seller.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('product.id'), nullable=False)