#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """
    User class that inherits from BaseModel.

    Attributes:
        email (str) = email of the user
        password (str) = password of the user
        first_name (str) = first name of user
        last_name (str) = last name of user

    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
