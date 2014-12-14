# TODO
from collections import namedtuple


class RawRecipe:
    """ Represents a recipe containing raw HTML data
    """
    pass


class ParsedRecipe:
    """ A recipe with text representation of ingredients
    """

    def __init__(self):
        self.url = None
        self.name = None
        self.ingredients = None
        self.preparation = None
        self.additionalAttributes = None


class ProcessedRecipe:
    """ Object representation of a recipe
    """

    def __init__(self):
        self.url = None
        self.name = None
        self.ingredients = None
        self.preparation = None
        self.additionalAttributes = None


class Ingredient:
    """ Class representing an ingredient
    """

    def __init__(self, name=None, amount=None):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return 'name: %s; amount: %s' % (self.name, self.amount)


class IngredientAmount(namedtuple('IngredientAmount', 'value, unit')):
    def __repr__(self):
        return 'value: %s; unit: %s' % (self.value, self.unit)
