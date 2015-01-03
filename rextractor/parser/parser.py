""" Module containing HTMLParser class. """
__author__ = 'Maciej Suchecki'

from bs4 import BeautifulSoup
from rextractor.model.recipe import ParsedRecipe


class HTMLParser:
    """ Class responsible for parsing RawRecipes and converting them to ParsedRecipes - it takes
    the recipe.html field and extracts all of the found information to create ParsedRecipe. """

    def parse_html(self, raw_recipes):
        """ Parses HTML in RawRecipes to extract text information.
        :param raw_recipes: list of RawRecipes to convert
        :return: list of ParsedRecipes created from RawRecipes
        """
        parsed_recipes = []

        for recipe in raw_recipes:
            parsed_recipes.append(self.__parse_recipe(recipe))

        return parsed_recipes

    # TODO move this particular implementation somewhere deeper - this method
    # should be universal, not bound to particular website like now!
    def __parse_recipe(self, recipe):
        """ Parses HTML from one RawRecipe and converts it to ParsedRecipe.
        :param recipe: any RawRecipe
        :return: ParsedRecipe created from given recipe
        """
        soup = BeautifulSoup(recipe.html)

        name = str(soup.select('h1.entry-title')[0].string)

        ingredients = []
        for li in soup.select('div#recipe-ingredients li'):
            ingredients.append(li.get_text())

        preparation = ''
        for p in soup.select('div#recipe-method p'):
            preparation += p.get_text() + '\n'

        # additional attributes
        new_recipe = ParsedRecipe(recipe.url, name, ingredients, preparation)
        attributes = {'description': soup.select('div#recipe-intronote'),
                      'portions': soup.select('span.yield'), 'cook_time': soup.select('span.cooktime'),
                      'prep_time': soup.select('span.preptime')}
        for key, value in attributes.items():
            if len(value) != 0:
                new_recipe.add_attribute(key, value[0].get_text())

        return new_recipe
