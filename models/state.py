#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """
    Simple model of a state.

    Attributes:
        name (str): Name of the state.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete")

    @property
    def cities(self):
        """
        Returns a list of City instances with state_id equals to the
        current State.id
        """
        from models import storage
        related_cities = []
        cities = storage.all(City)
        for city in cities.values():
            if city.state_id == self.id:
                related_cities.append(city)
        return related_cities
