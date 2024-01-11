from datetime import datetime
import models
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid


time = "%y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()

class BaseModel:
    """the base model class which serves as the base for all other class"""
    id = Column(String(60), nullable=False, unique=True, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __init__(self, *args, **kwargs):
        if kwargs:
            kwargs.pop("__class__", None)
            self.id = str(uuid.uuid4())
            for key, value in kwargs.items():
                setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """updates the newly created object time then crates it a new object and saves to th database"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        # returns a dictionary representation of the instance 
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = self.__class__.__name__
        if "created_at" in my_dict:
            my_dict["created_at"] = my_dict["created_at"].isoformat()
        if "updated_at" in my_dict:
            my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        if "_sa_instance_state" in my_dict.keys():
            del my_dict["_sa_instance_state"]
        return my_dict
    
    def delete(self):
        """deletes current instance from storage"""
        models.storage.delete(self)