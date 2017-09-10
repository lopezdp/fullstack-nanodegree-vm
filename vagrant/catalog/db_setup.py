import sys

# Configuration
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

# Classes
Base = declarative_base()

# Representation of sql tables as a Python class
class Restaurant(Base):

    # Tables
    __tablename__ = 'restaurant'

    # Mapper: Maps Python Objects to 
    # columns in our database
    name = Column (
        String(80), 
        nullable = False
    )

    id = Column (
        Integer, 
        primary_key = True
    )

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id,
        }

class MenuItem(Base):

    # Tables
    __tablename__ = 'menu_item'

    # Mapper: Maps Python Objects to 
    # columns in our database
    name = Column (
        String(80),
        nullable = False
    )

    id = Column (
        Integer, 
        primary_key = True
    )

    course = Column (
        String(250)
    )

    description = Column (
        String(250)
    )

    price = Column (
        String(8)
    )

    restaurantid = Column (
        Integer,
        ForeignKey('restaurant.id')
    )

    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # Returns object data in serialized format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course,
        }

# Insert at EOF
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

