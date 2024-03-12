#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime

class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.identifier = str(uuid4())
        self.creation_time = datetime.today()
        self.update_time = datetime.today()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "creation_time" or key == "update_time":
                    self.__dict__[key] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """Update update_time with the current datetime."""
        self.update_time = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        return {
            "id": self.identifier,
            "created_at": self.creation_time.isoformat(),
            "updated_at": self.update_time.isoformat(),
            "__class__": self.__class__.__name__
        }

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.identifier, self.__dict__)
