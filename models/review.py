#!/usr/bin/python3
"""
Defines review class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Define Reviews made by users"""
    place_id = ""
    user_id = ""
    text = ""
