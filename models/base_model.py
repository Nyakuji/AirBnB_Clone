#!/usr/bin/python3
"""
Parent class that will inherit
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """Defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """initializes all attributes"""
        self.id = str(uuid.uuid4())  # Assign id explicitly in the BaseModel
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        storage.new(self)

        if kwargs:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key in ('created_at', 'updated_at'):
                    value = datetime.strptime(value, date_format)
                if key != '__class__':
                    setattr(self, key, value)

    def __str__(self):
        """returns class name, id, and attribute dictionary"""
        class_name = "[" + self.__class__.__name__ + "]"
        attribute_dict = {
            k: v for (k, v) in
            self.__dict__.items() if v is not None
        }
        return f"{class_name} ({self.id}) {attribute_dict}"

    def save(self):
        """updates last update time"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """creates a new dictionary, adding a key and returning
        datetimes converted to strings"""
        new_dict = {}

        for key, value in self.__dict__.items():
            if key in ('created_at', 'updated_at'):
                new_dict[key] = value.strftime("%Y-%m-%dT%H:%M:%S.%f")
            elif value is not None:
                new_dict[key] = value

        new_dict['__class__'] = self.__class__.__name__
        return new_dict
