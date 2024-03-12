#!/usr/bin/python3
"""Defines the State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represent a state.

    Attributes:
        state_name (str): The name of the state.
    """

    state_name = ""
