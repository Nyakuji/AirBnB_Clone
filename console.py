#!/usr/bin/python3
"""Contains the entry point of the command interpreter"""
import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review


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

    class_mapping = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'City': City,
        'Amenity': Amenity,
        'State': State,
        'Review': Review
    }

    def help_help(self):
        """Prints help command description"""
        print("Provides a description of a given command")

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

        if args_list[0] not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
            return

        kwargs = {}
        for arg in args_list[1:]:
            if '=' in arg:
                key, value = arg.split('=')
                # Remove any quotes around the value
                value = value.strip('"\'')
                kwargs[key] = value

        selected_model = HBNBCommand.class_mapping[args_list[0]](**kwargs)
        print(selected_model.id)
        selected_model.save()

    def do_show(self, arg):
        """
        Prints the string representation
        of an instance based on the class name and id
        """

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')
        class_name = args[0]

        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            i_id = args[1].strip('"')
            all_objs = storage.all()

            for value in all_objs.values():
                if value.__class__.__name__ == class_name and value.id == i_id:
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

        args = arg.split(' ')
        class_name = args[0]

        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            instance_id = args[1].strip('"')
            all_objs = storage.all()

            for key, value in all_objs.items():
                ob_name = value.__class__.__name__
                ob_id = value.id

                if ob_name == class_name and ob_id == instance_id:
                    del value
                    del storage._FileStorage__objects[key]
                    storage.save()
                    return

            print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not
        on the class name
        """

        if not arg:
            print("** class name is missing **")
            return

        args = arg.split(' ')
        class_name = args[0]

        if class_name not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
        else:
            all_objs = storage.all()
            list_instances = []

            for key, value in all_objs.items():
                ob_name = value.__class__.__name__

                if ob_name == class_name:
                    list_instances.append(str(value))

            print(list_instances)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file)
        """
        if not arg:
            print("** class name missing **")
            return

        # concatenated_args = ""
        # for argv in arg.split(','):
        #     concatenated_args += argv

        args = shlex.split(arg)

        if args[0] not in HBNBCommand.__allowed_classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for key, objc in all_objs.items():
                ob_name = objc.__class__.__name__
                ob_id = objc.id

                if ob_name == args[0] and ob_id == args[1].strip('"'):
                    if len(args) < 3:
                        print("** attribute name missing **")
                    elif len(args) < 4:
                        print("** value missing **")
                    else:
                        setattr(objc, args[2], args[3])
                        storage.save()
                    return

            print("** no instance found **")

    def strip_clean(self, args):
        """strips the argument and return a string of command
        Args:
            args: input list of args
        Return:
            returns string of argumetns
        """
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """retrieve all instances of a class and
        retrieve the number of instances
        """
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.do_count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)

    def do_quit(self, line):
        """Quit command to exit the command interpreter"""
        return True

    def do_EOF(self, line):
        """EOF command to exit the command interpreter"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
