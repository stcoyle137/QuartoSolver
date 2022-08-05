import math
from itertools import product

class Attribute():
    current_id = 0
    def __init__(self, name_attribute, names_attribute_value, id = None):
        self.name = name_attribute

        if id != None:
            self.id = id
        else:
            self.id = Attribute.current_id
            Attribute.current_id += 1

        self.values = names_attribute_value

    def is_equal(self):
        pass


class BlankAttribute(Attribute):

    def __init__(self):
        super().__init__("blank", ["blank"], -1)

    @staticmethod
    def blank_token():
        return BlankAttribute()

class Token():
    def __init__(self, attribute_dict):
        # A attribute dict is in the form Attribute : Attribute_Value_Id
        self.attribute_dict = attribute_dict
        self.available = True
        self.whitespace = False
    def __str__(self):
        return "".join([str(self.attribute_dict[k]) for k in self.attribute_dict.keys()])

class BlankToken(Token):
    def __init__(self):
        super().__init__({BlankAttribute.blank_token() : 0})
        self.whitespace = True

class TokenManager():
    def __init__(self):
        self.attributes = []
        self.bank = []
        self.get_attribute_info_hardcoded()
        self.permutate_attributes()

    def get_attribute_info_user(self):
        pass

    def get_attribute_info_hardcoded(self):
        self.attribute_name = ["size", "shape", "color", "concavity"]
        self.attribute_value_dict_name = {"tall" : "size", "short" : "size",
                                          "square" : "shape", "circle" : "shape",
                                          "white" : "color", "black" : "color",
                                          "solid" : "concavity", "empty" : "concavity"}
        self.attributes = []
        for a in self.attribute_name:
            self.attributes.append(Attribute(a, [name for name in self.attribute_value_dict_name.keys() if self.attribute_value_dict_name[name] == a]))

    def permutate_attributes(self):
        self.bank = []
        tmp_list =[]
        for attribute in self.attributes:
            tmp_list.append([i for i in range(0, len(attribute.values))])

        # Voodoo magic that works the same as 4 hours of work
        list_of_perms = list(product(*tmp_list))

        for l in list_of_perms:
            dict_builder = {}
            for i in range(0,len(l)):
                dict_builder[self.attributes[i]] = l[i]
            self.bank.append(Token(dict_builder))

    def get_bank(self):
        return self.bank

    def get_remaining_bank(self):
        bank_remaining = []
        for i in range(0, len(self.bank)):
            if not self.bank[i].available:
                continue
            bank_remaining.append((i,self.bank[i]))
        return bank_remaining


    def get_included_attributes(self):
        return self.attributes

    def get_remaining_bank_str(self):
        string_builder = ""
        for i in range(0, len(self.bank)):
            if not self.bank[i].available:
                continue
            string_builder += str(i) + " : "
            string_builder += str(self.bank[i])
            string_builder += "\n"
        return string_builder

    def choose_token(self, index_of_token):
        t = self.bank[index_of_token]
        if t.available:
            t.available = False
            return t

    def __str__(self):
        str_builder = "id | token | available\n"
        for i in range(len(self.bank)):
            str_builder += str(i) + " " + (" " * (max(len(str(len(self.bank))),2) - len(str(i)))) + "| "
            str_builder += str(self.bank[i]) + (" " * (max(len(str(self.bank[i])), 5) - len(str(self.bank[i]))))+ " | "
            str_builder += str(self.bank[i].available) + "\n"
        return str_builder
