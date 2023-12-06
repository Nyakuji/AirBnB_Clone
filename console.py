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

    __allowed_classes = ['BaseModel', 'User', 'Amenity', 'Place', 'City', 'State', 'Review']
    __allowed_commands = ['create', 'show', 'update', 'all', 'destroy', 'count']

    # def precmd(self, arg):
    #     """Parses command input"""
    #     if '.' in arg and '(' in arg and ')' in arg:
    #         class_method = arg.split('.')
    #         command_and_args = class_method[1].split('(')
    #         if class_method[0] in HBNBCommand.allowed_classes and command_and_args[0] in HBNBCommand.allowed_commands:
    #             args = f"{command_and_args[0]}{class_method[0]} {args[0]}"
    #         return arg

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

    def do_create(self, type_model):
        """Creates an instance according to a given class"""

        if not type_model:
            print("** class name missing **")
        elif type_model not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        else:
            class_mapping = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'City': City,
            'Amenity': Amenity,
            'State': State,
            'Review': Review
        }

        selected_model = class_mapping[type_model]()
        print(selected_model.id)
        selected_model.save()

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id"""

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

            for key, value in all_objs.items():
                if value.__class__.__name__ == class_name and value.id == instance_id:
                    print(value)
                    return
            print("** no instance found **")
    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id (save the change into the JSON file)"""

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

            for key, value in all_objs.items():
                if value.__class__.__name__ == class_name and value.id == instance_id:
                    del value
                    del storage._FileStorage__objects[key]
                    storage.save()
                    return
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on the class name."""

        if not arg:
            print("** class name missing **")
            return

        class_name, *_ = arg.split()

        if class_name not in HBNBCommand.__allowed_classes:
            print("** Class doesn't exist **")
        else:
            all_objs = storage.all()
            list_instances = [str(value) for value in all_objs.values() if value.__class__.__name__ == class_name]
            print(list_instances)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file)"""

        if not arg:
            print("** Class name missing **")
            return

        args = shlex.split(arg.replace(',' ''))

        if args[0] not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            all_objs = storage.all()
            for key, obj_instance in all_objs.items():
                obj_name = obj_instance.__class__.__name__
                obj_id = obj_instance.id
                if obj_name == args[0] and obj_id == args[1].strip('"'):
                    setattr(obj_instance, args[2], args[3])
                    storage.save()
                    return

            print("** No instance found **")

    def do_quit(self, line):
        """ Quit command to exit the command interpreter """
        return True

    def do_EOF(self, line):
        """ EOF command to exit the command interpreter """
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()

