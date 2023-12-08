#!/usr/bin/python3
'''This is unittests is for the console.py'''

import os
import unittest
import contextlib
import pep8
from models.engine.file_storage import FileStorage
from console import HBNBCommand

class TestHBNBCommand(unittest.TestCase):
    '''Some unittests to test the HBNB command interpreter'''

    @classmethod
    def setUpClass(cls):
        """
        Set up the class by renaming a file and initializing the HBNBCommand class.

        This method is a class method (decorated with @classmethod) and is intended
        to be called once for the entire class. It performs the following steps:

        1. Renames the file "file.json" to ".tmp" using the os.rename() function.
            If the file does not exist, it suppresses the IOError exception.

        2. Initializes the HBNBCommand class and assigns it to the class variable cls.HBNB.

        Parameters:
            cls (type): The class object itself.

        Returns:
            None
        """

        with contextlib.suppress(IOError):
            os.rename("file.json", ".tmp")
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        with contextlib.suppress(IOError):
            os.rename('.tmp', 'file.json')
        del cls.HBNB

    def test_pep8_console(self):
        '''Tests that console.py conforms to PEP8'''
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors.")

if __name__ == "__main__":
    unittest.main()
