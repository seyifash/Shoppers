from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
import models

class Order(BaseModel, Base):
    """creates a new product"""
    __tablename__ = 'order'
    productName = Column(String(255), nullable=False)
    productPrice = Column(Integer, nullable=False)
    productQuantity = Column(Integer, nullable=False)
    productSize = Column(String(255), nullable=False)
    productColor = Column(String(255), nullable=False)
    paymentStatus = Column(String(255), nullable=False)
    transaction_id = Column(String(200), nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    seller_id = Column(String(60), ForeignKey('seller.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('product.id'), nullable=False)
    
    
    @property
    def get_total(self):
        total = self.productPrice * self.productQuantity
        return total
    
    @property
    def get_all_total(self):
        total = sum(order.productTotal for order in self)
        return total
    
    @property
    def get_all_quantity(self):
        total_quantity = sum(order.productQuantity for order in self)
        return total_quantity
        
    @staticmethod
    def get_order_total(user_id):
        all_orders = models.storage.get_orders_by_user_id(Order, user_id)
        total = sum(order.get_total for order in all_orders)
        return total
    
    @staticmethod
    def get_order_quant(user_id):
        all_orders = models.storage.get_orders_by_user_id(Order, user_id)
        total = sum(order.productQuantity for order in all_orders)
        return total   