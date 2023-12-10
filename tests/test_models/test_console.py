#!/usr/bin/python3
'''This is unittests is for the console.py'''

from io import StringIO
import os
import unittest
import contextlib
from unittest.mock import patch
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

    def setUp(self):
        '''Resets FileStorage objects dictionary'''
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        '''Delete any created file.json'''
        with contextlib.suppress(IOError):
            os.remove('file.json')

    def test_pep8_console(self):
        '''Tests that console.py conforms to PEP8'''
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors.")

    def test_docstrings(self):
        '''Checks for availability of docstrings in files'''
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.help_help.__doc__)

    def test_emptyline(self):
        '''Test empty line input'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd('\n')
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        '''Test quit command'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd('quit')
            self.assertEqual('', f.getvalue())

    def test_create_errors(self):
        '''Test create command errors'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd('create')
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd('create MyModel')
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_create(self):
        """Test create command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            us = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            st = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Place")
            pl = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create City")
            ct = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Review")
            rv = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Amenity")
            am = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(bm, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            self.assertIn(us, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertIn(st, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            self.assertIn(pl, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all City")
            self.assertIn(ct, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Review")
            self.assertIn(rv, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(am, f.getvalue())

    def test_create_kwargs(self):
        """Test create command with kwargs."""
        with patch("sys.stdout", new=StringIO()) as f:
            call = ('create Place city_id="0001" name="My_house" ''number_rooms=4 latitude=37.77 longitude=a'
                    )
            self.HBNB.onecmd(call)
            pl = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            output = f.getvalue()
            self.assertIn(pl, output)
            self.assertIn("'city_id': '0001'", output)
            self.assertIn("'name': 'My house'", output)
            self.assertIn("'number_rooms': 4", output)
            self.assertIn("'latitude': 37.77", output)
            self.assertNotIn("'longitude'", output)

    def test_show(self):
        """Test show command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command input."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all(self):
        """Test all command input."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test update command input."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()

