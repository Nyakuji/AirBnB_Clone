#!/usr/bin/python3
"""
Class FileStorage that serializes instances
to a JSON file and deserializes JSON file to instances
"""
import json
import os


class FileStorage:
    """Class that serializes instances to a
    JSON file and deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        dictionary = {
            key: value.to_dict()
            for key, value in FileStorage.__objects.items()
            }

        with open(FileStorage.__file_path, 'w') as f:
            json.dump(dictionary, f)

    def reload(self):
        """Deserializes __objects from the JSON file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.city import City
        from models.amenity import Amenity
        from models.state import State
        from models.review import Review

        class_mapping = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'City': City,
            'Amenity': Amenity,
            'State': State,
            'Review': Review
            }

        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    class_name = value['__class__']
                    if class_name in class_mapping:
                        self.new(class_mapping[class_name](**value))
