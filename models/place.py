#!/usr/bin/python3
"""Defines a class Place."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
import models


place_amenity = Table("place_amenity", Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """
    A simple model of a place.

    Attributes:
        city_id (str): city ID
        user_id (str): user ID
        name (str): name of the place
        description (str): description of the place
        number_rooms (int): number of rooms of the place
        number_bathrooms (int): number of bathrooms of the place
        max_guest (int): maximum guests of the place
        price_by_night (int): price by night of the place
        latitude (float): latitude of the place
        longitude (float): longitude of the place
        amenity_ids (list): list of Amenity IDs
    """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 back_populates="place_amenities",
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """Getter method for returning a list of reviews"""
            reviews_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            """
            Getter method to return list of amenities based on amenity_id
            that contains amenity.id linked to Place
            """
            amenities_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, value):
            """Setter method for amenity_ids"""
            if isinstance(value, Amenity):
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value.id)
