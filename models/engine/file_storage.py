#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        file_path (str): The name of the file to save objects to.
        objects (dict): A dictionary of instantiated objects.
    """
    file_path = "file.json"
    objects = {}

    def all(self):
        """Return the dictionary objects."""
        return FileStorage.objects

    def new(self, object_instance):
        """Set in objects object_instance with key <object_class_name>.id"""
        class_name = object_instance.__class__.__name__
        FileStorage.objects["{}.{}".format(class_name, object_instance.id)] = object_instance

    def save(self):
        """Serialize objects to the JSON file file_path."""
        object_dict = FileStorage.objects
        serialized_objects = {obj: object_dict[obj].to_dict() for obj in object_dict.keys()}
        with open(FileStorage.file_path, "w") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserialize the JSON file file_path to objects, if it exists."""
        try:
            with open(FileStorage.file_path) as file:
                object_dict = json.load(file)
                for serialized_object in object_dict.values():
                    class_name = serialized_object["__class__"]
                    del serialized_object["__class__"]
                    self.new(eval(class_name)(**serialized_object))
        except FileNotFoundError:
            return
