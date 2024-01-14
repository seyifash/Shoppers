from models.base_model import BaseModel, Base
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy import String, Column, Text, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """creates a new product"""
    __tablename__ = 'product'
    BrandName = Column(String(255), nullable=False)
    productPrice = Column(Integer, nullable=False)
    productColor = Column(Text, nullable=False)
    productSize = Column(Text, nullable=False)
    productMeasurement = Column(Text, nullable=False)
    productDescription = Column(Text, nullable=False)
    productCategory = Column(String(255), nullable=False)
    seller_id = Column(String(60), ForeignKey('seller.id'), nullable=False)
    category_id = Column(String(60), ForeignKey('category.id'), nullable=False)
    
    category = relationship('Category', back_populates='products_category')
    image = relationship('ProductImage', backref='product')


class ProductImage(BaseModel, Base):
    __tablename__ = 'product_image'
    image_filename = Column(String(255), nullable=False)
    product_id = Column(String(60), ForeignKey('product.id'), nullable=False)