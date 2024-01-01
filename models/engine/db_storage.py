from models.base_model import BaseModel, Base
from models.user import User
from models.product import Product
from models.seller_user import Seller
from models.order import Order
from models.categories import Category
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from datetime import datetime, timedelta

classes = {"User": User, "Product": Product, "Seller": Seller, "Order": Order, "Category": Category}

class DBStorage:
    """ data storage using sqlalchemy"""
    __engine = None
    __session =  None
    
    def __init__(self):
        """Initialization."""
        user = 'Shoppers'
        pwd = 'shoppers1996'
        host = 'localhost'
        db = 'shoppers_db'  
        self.__engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(user, pwd, host, db), pool_pre_ping=True)
            
    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
    
    def new(self, obj):
        """new objects are created and added """
        self.__session.add(obj)
        
    def save(self):
        """save the newly created obj to the database"""
        self.__session.commit()
        
    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)
            
    def reload(self):
        Base.metadata.create_all(self.__engine)
        session =  sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)
        
    def close(self):
        """removes a session"""
        if self.__session:
            self.__session.remove()
        
    def count(self, cls=None):
        count = 0
        if cls:
            if cls in classes.values():
                count = len(self.all(cls))
        else:
            count = len(self.all())
        
        return count
    
    def get_by_email(self, cls, email):
        if cls:
            if cls in classes.values():
                return self.__session.query(cls).filter_by(email=email).first()
            return None
        
    def get_user_by_id(self, cls, user_id):
        """Get a user by ID."""
        if cls:
            if cls in classes.values():
                return self.__session.query(cls).get(user_id )
        return None
    
    def get_orders_by_user_id(self, cls, user_id):
        if cls in classes.values():
            cls_items = self.all(cls)
            l = [l for l in cls_items.values() if l.user_id == user_id]
            return l
        return None
    
    def get_sellers_orders(self, seller_id):
        results = []
        seller_class = classes.get('Seller')
        if seller_class:
            seller = self.get_user_by_id(seller_class, seller_id)
        if seller:
            orders = seller.orders
            for order in orders:
                user = self.get_user_by_id(User, order.user_id)
                results.append((order, user))

        return results 
    
    def today_sales(self, seller_id):
        total_order = 0
        percentage_of_order = 0
        base_value = 100
        seller = self.get_user_by_id(Seller, seller_id)
        if seller:
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            todays_order = [order for order in seller.orders if today_start <= order.created_at < today_end]
            total_order = sum(order.total for order in todays_order)
            if total_order > 0:
                percentage_of_order = (total_order / base_value) * 100
                
        return total_order, percentage_of_order
    
    def total_sales(self, seller_id):
        total_order = 0
        percentage_of_order = 0
        base_value = 100
        seller = self.get_user_by_id(Seller, seller_id)
        if seller:
            todays_order = [order for order in seller.orders ]
            total_order = sum(order.total for order in todays_order)
            if total_order > 0:
                percentage_of_order = (total_order / base_value) * 100
                
        return total_order, percentage_of_order
    
    def total_orders(self, seller_id):
        total_order = 0
        percentage_of_order = 0
        base_value = 100
        seller = self.get_user_by_id(Seller, seller_id)
        if seller:
            total_order = len(seller.orders)
            if total_order > 0:
                percentage_of_order = (total_order / base_value) * 100 
            
        return total_order, percentage_of_order
            