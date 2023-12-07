#!/usr/bin/python3
"""Module for FileStorage test"""
import unittest
import tempfile
import shutil
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import os
import json


class FileStorageTests(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory for testing"""
        self.temp_dir = tempfile.mkdtemp()
        FileStorage._FileStorage__file_path = os.path.join(self.temp_dir,'file.json')
        self.storage = FileStorage()
        self.my_model = BaseModel()

    def tearDown(self):
        """Clean up the temporary directory"""
        shutil.rmtree(self.temp_dir)

    def test_class_instance(self):
        """Check if an instance of FileStorage is created"""
        self.assertIsInstance(storage, FileStorage)

    def test_store_base_model(self):
        """Test saving, reloading, and updating a BaseModel instance"""
        my_model = BaseModel()
        my_model.full_name = "BaseModel Instance"
        my_model.save()

        bm_dict = my_model.to_dict()
        all_objs = storage.all()
        key = f"{bm_dict['__class__']}.{bm_dict['id']}"

        self.assertIn(key, all_objs)
        self.assertEqual(all_objs[key].full_name, "BaseModel Instance")

    def test_store_base_model2(self):
        """Test save, reload, and update functions"""
        # Set the first name
        self.my_model.my_name = "First name"
        self.my_model.save()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()
        key = f"{bm_dict['__class__']}.{bm_dict['id']}"

        self.assertIn(key, all_objs)
        self.assertEqual(self.my_model.my_name, "First name")

        create1 = bm_dict['created_at']
        update1 = bm_dict['updated_at']

        # Set the second name
        self.my_model.my_name = "Second name"
        self.my_model.save()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        self.assertIn(key, all_objs)

        create2 = bm_dict['created_at']
        update2 = bm_dict['updated_at']
        self.assertEqual(create1, create2)
        self.assertNotEqual(update1, update2)
        self.assertEqual(self.my_model.my_name, "Second name")

    def test_has_attributes(self):
        """Test if FileStorage has the expected attributes"""
        self.assertTrue(hasattr(FileStorage, '_FileStorage__file_path'))
        self.assertTrue(hasattr(FileStorage, '_FileStorage__objects'))

    def test_save(self):
        """Verify if JSON exists"""
        self.my_model.save()
        self.assertTrue(os.path.exists(storage._FileStorage__file_path))
        self.assertEqual(storage.all(), storage._FileStorage__objects)

    def test_save_FileStorage(self):
        """Test if 'save' method is working correctly"""

        # Save the model to the storage
        self.storage.new(self.my_model)
        self.storage.save()

        # Read the content of the saved JSON file
        with open(FileStorage._FileStorage__file_path, 'r') as fd:
            saved_data = json.load(fd)

        # Get the key for the model in the saved data
        model_key = f"{self.my_model.__class__.__name__}.{self.my_model.id}"

        # Check if the saved data contains the expected information .
        self.assertIn(model_key, saved_data)

        # Compare each attribute in the saved data with the model's attributes
        for key, value in self.my_model.to_dict().items():
            self.assertEqual(saved_data[model_key][key], value)

    def test_cleanup(self):
        """Ensure no artifacts are left after running tests"""
        # Ensure that the temporary directory is empty after each test.
        self.assertEqual(os.listdir(self.temp_dir), [])


if __name__ == '__main__':
    unittest.main()
