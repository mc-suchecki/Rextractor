""" Module containing HTMLParser class. """
__author__ = 'Maciej Suchecki'

from rextractor.model.websites import Websites
from rextractor.parser.parsers.simply_recipes import SimplyRecipesParser


class HTMLParser:
    """ Class responsible for parsing RawRecipes and converting them to ParsedRecipes - it takes
    the recipe.html field and extracts all of the found information to create ParsedRecipe. """

    # dictionary used for mapping Recipes to proper Parsers
    parsers = {Websites.SIMPLY_RECIPES: SimplyRecipesParser()}

    def parse_html(self, raw_recipes):
        """ Parses HTML in RawRecipes to extract text information.
        :param raw_recipes: list of RawRecipes to convert
        :return: list of ParsedRecipes created from RawRecipes
        """
        parsed_recipes = []

        for recipe in raw_recipes:
            parsed_recipes.append(self.__parse_recipe(recipe))

        return parsed_recipes

    def __parse_recipe(self, recipe):
        """ Gets proper Parser for Recipe with given source and calls parse_recipe method from it.
        :param recipe: any RawRecipe
        :return: ParsedRecipe created from given recipe
        """
        return self.parsers[recipe.source].parse_recipe(recipe)
