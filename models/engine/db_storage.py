#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import os
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    """This class manages storage of hbnb models in mysql database"""
    __engine = None
    __session = None

    def __init__(self):
        from sqlalchemy import create_engine

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            os.getenv("HBNB_MYSQL_USER"),
            os.getenv("HBNB_MYSQL_PWD"),
            os.getenv("HBNB_MYSQL_HOST"),
            os.getenv("HBNB_MYSQL_DB")
            ), pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class name"""
        result_dict = {}
        classes = []
        class_mapping = {
                    'User': User,
                    'Place': Place,
                    'State': State,
                    'City': City,
                    'Amenity': Amenity,
                    'Review': Review
                  }

        if cls is not None:
            classes.append(cls)
        else:
            classes.extend(class_mapping.values())

        for cls in classes:
            #print("*" * 5 + str(type(cls)) + "*"*5)
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                result_dict[key] = obj

        return result_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ calls remove() method on the private session attribute """
        self.__session.close()
