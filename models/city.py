#!/usr/bin/python3
"""Defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a city.

    Attributes:
        city_state_id (str): The state id.
        city_name (str): The name of the city.
    """

    city_state_id = ""
    city_name = ""
