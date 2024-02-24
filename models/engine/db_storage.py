#!/usr/bin/python3
"""Defines DBstorage"""
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


models = {"User": User, "State": State, "City": City,
          "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    """A dbstorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """initializes dbstorage"""
        USER = getenv('HBNB_MYSQL_USER')
        PWD = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(USER, PWD, HOST, DB),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns current database session"""
        objs = {}
        if cls is not None:
            for obj in self.__session.query(cls).all():
                objs[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for model in models:
                for obj in self.__session.query(models[model]):
                    objs[obj.__class__.__name__ + '.' + obj.id] = obj
        return objs

    def new(self, obj):
        """Adds object to the current session"""
        self.__session.add(obj)

    def save(self):
        """Saves to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload tables in the database"""
        # Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)

    def close(self):
        """ Public method to close the session"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve one object"""
        if cls and id:
            return self.__session.query(cls).filter_by(id=id).first()

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls:
            return self.__session.query(cls).count()
        else:
            total_count = 0
            for clss in classes:
                total_count += self.__session.query(classes[clss]).count()
