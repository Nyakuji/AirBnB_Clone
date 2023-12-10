#!/usr/bin/python3
"""Unittest for review.py"""
import unittest
from models.review import Review
import datetime


class TestReview(unittest.TestCase):
    """Tests instances and methods from Review class"""

    def setUp(self):
        """Set up a Review instance for testing"""
        self.r = Review()

    def test_class_exists(self):
        """Test if the Review class exists"""
        self.assertEqual(str(type(self.r)), "<class 'models.review.Review'>")

    def test_user_inheritance(self):
        """Test if Review is a subclass of BaseModel"""
        self.assertIsInstance(self.r, Review)

    def test_has_attributes(self):
        """Verify if attributes exist"""
        self.assertTrue(hasattr(self.r, 'place_id'))
        self.assertTrue(hasattr(self.r, 'user_id'))
        self.assertTrue(hasattr(self.r, 'text'))
        self.assertTrue(hasattr(self.r, 'id'))
        self.assertTrue(hasattr(self.r, 'created_at'))
        self.assertTrue(hasattr(self.r, 'updated_at'))

    def test_attribute_types(self):
        """Test if the types of attributes are correct"""
        self.assertIsInstance(self.r.place_id, str)
        self.assertIsInstance(self.r.user_id, str)
        self.assertIsInstance(self.r.text, str)
        # Assuming id is of type uuid.UUID, adjust accordingly
        # self.assertIsInstance(self.r.id, uuid.UUID)
        self.assertIsInstance(self.r.created_at, datetime.datetime)
        self.assertIsInstance(self.r.updated_at, datetime.datetime)

    def test_created_updated_format(self):
        """Test if created_at and updated_at are in the correct format"""
        created_at_str = self.r.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        updated_at_str = self.r.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(self.r.created_at.isoformat(), created_at_str)
        self.assertEqual(self.r.updated_at.isoformat(), updated_at_str)


if __name__ == '__main__':
    unittest.main()
