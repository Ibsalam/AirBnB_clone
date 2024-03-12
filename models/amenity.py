#!/usr/bin/python3
"""Defines the Amenity class."""
from models.base_model import BaseModel

class Amenity(BaseModel):
    """Represent an amenity.

    Attributes:
        amenity_name (str): The name of the amenity.
    """

    amenity_name = ""
