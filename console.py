#!/usr/bin/python3
"""contains the entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review
import json
import shlex


class HBNBCommand(cmd.Cmd):
    """Command processor for HBNB project"""

    prompt = "(hbnb) "

    __allowed_classes = [
        'BaseModel',
        'User',
        'Amenity',
        'Place',
        'City',
        'State',
        'Review'
        ]
    __allowed_commands = [
        'create',
        'show',
        'update',
        'all',
        'destroy',
        'count'
        ]

    def help_help(self):
        """Prints help command description"""
        print("Provides description of a given command")

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_count(self, cls_name):
        """Counts the number of instances of a class"""
        count = 0
        all_objs = storage.all()
        for key, value in all_objs.items():
            class_name = key.split('.')
            if class_name[0] == cls_name:
                count += 1
        print(count)

    def do_create(self, args):
        """Creates an instance according to a given class with attributes"""

        # Split the arguments into class name and attributes
        args_list = shlex.split(args)
        if len(args_list) == 0:
            print("** class name missing **")
            return

        class_name = args_list[0]

        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
            return

        # Extract attributes and their values from the arguments
        attributes = {}
        for arg in args_list[1:]:
            # Split each argument to extract attribute and value
            split_arg = arg.split("=")
            attr_name = split_arg[0]
            attr_value = split_arg[1].strip('"')
            attributes[attr_name] = attr_value

        # Create an instance of the specified class
        class_mapping = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'City': City,
            'Amenity': Amenity,
            'State': State,
            'Review': Review
        }

        if class_name in class_mapping:
            selected_model = class_mapping[class_name]()
            # Set attributes for the instance
            for attr, value in attributes.items():
                setattr(selected_model, attr, value)

            print(selected_model.id)
            selected_model.save()
        else:
            print("** class doesn't exist **")


    def do_show(self, arg):
        """
        Prints the string representation
        of an instance based on the class name and id
        """

        if not arg:
            print("** class name missing **")
            return

        class_name, *instance_id = arg.split()

        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        elif not instance_id:
            print("** instance id missing **")
        else:
            instance_id = instance_id[0].strip('"')
            all_objs = storage.all()
            # class_match = value.__class__.__name__ == class_name
            # id_match = value.id == instance_id
            for key, value in all_objs.items():
                if value.__class__.__name__ == class_name and value.id == instance_id:
                    print(value)
                    return
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name
        and id (save the change into the JSON file)
        """

        if not arg:
            print("** class name missing **")
            return

        class_name, *instance_id = arg.split(" ")

        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        elif not instance_id:
            print("** instance id missing **")
        else:
            instance_id = instance_id[0].strip('"')
            all_objs = storage.all()

            for key, value in all_objs.items():
                className = value.__class__.__name__ == class_name
                instanceId = value.id == instance_id
                if className and instanceId:
                    del value
                    del storage._FileStorage__objects[key]
                    storage.save()
                    return
            print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of
        all instances based or not on the class name.
        """

        if not arg:
            print("** class name missing **")
            return

        class_name, *_ = arg.split()

        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        else:
            all_objs = storage.all()

            def condition(value):
                return (value.__class__.__name__ == class_name)
            list_instances = [
                str(value)
                for value in all_objs.values()
                if condition(value)
                ]
            print(list_instances)

    def do_update(self, arg):
        """
        Updates an instance based on the class name
        and id by adding or updating attribute
        (save the change into the JSON file)
        """

        if not arg:
            print("** class name missing **")
            return

        args = shlex.split(arg, " ")
        # print (args, len(args))

        if args[0] not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        obj_key = args[0] + '.' + args[1]
        all_objs = storage.all()

        if obj_key not in all_objs:
            print("** no instance found **")
            return
        elif len(args) < 3:
            print("** attribute name missing **")
            return
        elif len(args) < 4:
            print("** value missing **")
            return

        obj_instance = all_objs[obj_key]
        setattr(obj_instance, args[2], args[3])
        storage.save()

    def do_quit(self, line):
        """ Quit command to exit the command interpreter """
        return True

    def do_EOF(self, line):
        """ EOF command to exit the command interpreter """
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
