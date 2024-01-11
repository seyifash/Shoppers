from models.base_model import BaseModel, Base
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy import String, Column, Text, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """creates a new product"""
    __tablename__ = 'product'
    BrandName = Column(String(255), nullable=False)
    productPrice = Column(Integer, nullable=False)
    productSize = Column(Text, nullable=False)
    productDescription = Column(Text, nullable=False)
    productCategory = Column(String(255), nullable=False)
    image = relationship('ProductImage', backref='product')
    seller_id = Column(String(60), ForeignKey('seller.id'), nullable=False)
    category_id = Column(String(60), ForeignKey('category.id'), nullable=False)
    
    category = relationship('Category', back_populates='products_category')

class ProductImage(BaseModel, Base):
    __tablename__ = 'product_image'
    product_id = Column(String(255), ForeignKey('product.id'), nullable=False)
    image_filename = Column(String(255), nullable=False)
    