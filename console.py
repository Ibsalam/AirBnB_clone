#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg_str):
    curly_braces = re.search(r"\{(.*?)\}", arg_str)
    brackets = re.search(r"\[(.*?)\]", arg_str)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg_str)]
        else:
            lexer = split(arg_str[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg_str[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        command_prompt (str): The command prompt.
    """

    command_prompt = "(hbnb) "
    valid_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def empty_line(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default_action(self, arg):
        """Default behavior for cmd module when input is invalid"""
        action_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_parts = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_parts[1])
            if match is not None:
                action_parts = [arg_parts[1][:match.span()[0]], match.group()[1:-1]]
                if action_parts[0] in action_dict.keys():
                    call = "{} {}".format(arg_parts[0], action_parts[1])
                    return action_dict[action_parts[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_exit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF_signal(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create_instance(self, arg):
        """Usage: create_instance <class>
        Create a new class instance and print its id.
        """
        arg_list = parse(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.valid_classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

    def do_display_instance(self, arg):
        """Usage: display_instance <class> <id> or <class>.display_instance(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_list = parse(arg)
        instance_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.valid_classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in instance_dict:
            print("** no instance found **")
        else:
            print(instance_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def do_delete_instance(self, arg):
        """Usage: delete_instance <class> <id> or <class>.delete_instance(<id>)
        Delete a class instance of a given id."""
        arg_list = parse(arg)
        instance_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.valid_classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in instance_dict.keys():
            print("** no instance found **")
        else:
            del instance_dict["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def display_all_instances(self, arg):
        """Usage: display_all_instances or display_all_instances <class> or <class>.display_all_instances()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arg_list = parse(arg)
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.valid_classes:
            print("** class doesn't exist **")
        else:
            instance_list = []
            for instance in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == instance.__class__.__name__:
                    instance_list.append(instance.__str__())
                elif len(arg_list) == 0:
                    instance_list.append(instance.__str__())
            print(instance_list)

    def count_instances(self, arg):
        """Usage: count_instances <class> or <class>.count_instances()
        Retrieve the number of instances of a given class."""
        arg_list = parse(arg)
        count = 0
        for instance in storage.all().values():
            if arg_list[0] == instance.__class__.__name__:
                count += 1
        print(count)

    def update_instance(self, arg):
        """Usage: update_instance <class> <id> <attribute_name> <attribute_value> or
       <class>.update_instance(<id>, <attribute_name>, <attribute_value>) or
       <class>.update_instance(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        arg_list = parse(arg)
        instance_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if arg_list[0] not in HBNBCommand.valid_classes:
            print("** class doesn't exist **")
            return False
        if len(arg_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in instance_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_list) == 4:
            instance = instance_dict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in instance.__class__.__dict__.keys():
                val_type = type(instance.__class__.__dict__[arg_list[2]])
                instance.__dict__[arg_list[2]] = val_type(arg_list[3])
            else:
                instance.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            instance = instance_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for key, value in eval(arg_list[2]).items():
                if (key in instance.__class__.__dict__.keys() and
                        type(instance.__class__.__dict__[key]) in {str, int, float}):
                    val_type = type(instance.__class__.__dict__[key])
                    instance.__dict__[key] = val_type(value)
                else:
                    instance.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
