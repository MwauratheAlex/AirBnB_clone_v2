#!/usr/bin/python3
""" Place Module for HBNB project """
import os
import models
from models.base_model import BaseModel
from models.amenity import Amenity
from models.base_model import Base

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table("place_amenity", Base.metadata,
                      Column(
                          "place_id",
                          String(60),
                          ForeignKey("places.id"),
                          primary_key=True,
                          nullable=False),
                      Column(
                          "amenity_id",
                          String(60),
                          ForeignKey("amenities.id"),
                          primary_key=True,
                          nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []


    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place", cascade="all, delete")
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def reviews(self):
            all_reviews = models.storage.all(Review)
            place_reviews = []

            for review in all_reviews:
                if self.id == review.place_id:
                    place_reviews.append(review)

            return place_reviews

        @property
        def amenities(self):
            all_amenities = models.storage.all(Amenity)
            place_amenities = []

            for amenity in all_amenities:
                if amenity.id in self.amenity_ids:
                    place_amenities.append(amenity)

            return place_amenities

        @amenities.setter
        def amenities(self, amenity):
            if type(amenity) == Amenity:
                self.amenity_ids.append(amenity.id)
