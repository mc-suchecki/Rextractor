""" Classes representing various types of Recipes - on various stages of processing. """
from collections import namedtuple


class RawRecipe:
    """ A recipe containing only raw HTML code downloaded from a website. """
    url = ''
    html = ''

    def __init__(self, url, html):
        self.url = url
        self.html = html

    def __str__(self):
        return 'URL: ' + self.url + '\nHTML:\n' + str(self.html)


class AttributesDict(dict):
    """ Dictionary with limited types of keys used in ParsedRecipe. """
    _keys = ['description', 'portions', 'cook_time', 'prep_time']

    def __setitem__(self, key, val):
        if key not in AttributesDict._keys:
            raise KeyError
        dict.__setitem__(self, key, val)


class ParsedRecipe:
    """ A recipe parsed by HTML parser - data is now divided into variables (name, ingredients, preparation, etc.). """
    url = ''
    name = ''
    ingredients = []
    preparation = ''
    additional_attributes = AttributesDict()

    def __init__(self, url, name, ingredients, preparation):
        self.url = url
        self.name = name
        self.ingredients = ingredients
        self.preparation = preparation

    def add_attribute(self, key, value):
        """ Adds additional attribute to the recipe. Throws KeyError if key is not valid.
        :param key: one of the keys defined in AttributesDict
        :param value: any string
        """
        self.additional_attributes[key] = value

    def __str__(self):
        string = '\nURL: ' + self.url + '\n'
        string += 'Name: ' + self.name + '\n'
        string += 'Ingredients: \n'
        for ingredient in self.ingredients:
            string += '- ' + str(ingredient) + '\n'
        string += 'Preparation: ' + self.preparation + '\n'
        for key, value in self.additional_attributes.items():
            string += key + ': ' + value + '\n'
        return string


class ProcessedRecipe(ParsedRecipe):
    """ Final representation of a recipe - with text processed by natural language processor. """
    pass


class Ingredient:
    """ Class representing an ingredient. """

    def __init__(self, name=None, amount=None):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return 'name: %s; amount: %s' % (self.name, self.amount)

    def __eq__(self, other):
        return self.name == other.name and self.amount == other.amount


class IngredientAmount(namedtuple('IngredientAmount', 'value, unit')):
    def __repr__(self):
        return 'value: %s; unit: %s' % (self.value, self.unit)

