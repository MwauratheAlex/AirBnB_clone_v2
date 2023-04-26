#!/usr/bin/python3
""" State Module for HBNB project """
import os

from models.base_model import BaseModel
from models.base_model import Base

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", back_populates="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """returns the list of City instances with state_id equals
            to the current State.id"""
            from models import storage
            from models.city import City

            all_cities = storage.all(City)
            state_cities = []

            for city in all_cities:
                if self.id == city.state_id:
                    state_cities.append(city)

            return state_cities
