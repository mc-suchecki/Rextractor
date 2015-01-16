__author__ = 'Maciej Suchecki'

# TODO check this file with pylint

from bs4 import BeautifulSoup
from rextractor.model.recipe import ParsedRecipe


class SimplyRecipesParser():

    @staticmethod
    def parse_recipe(recipe):
        """ Parses HTML from one RawRecipe and converts it to ParsedRecipe.
        :param recipe: any RawRecipe with type SIMPLY_RECIPES
        :return: ParsedRecipe created from given recipe
        """
        soup = BeautifulSoup(recipe.html)

        name = str(soup.select('h1.entry-title')[0].string)

        ingredients = []
        for li in soup.select('div#recipe-ingredients li'):
            ingredients.append(li.get_text())

        preparation = []
        for p in soup.select('div#recipe-method p'):
            text = p.get_text().strip()
            if text != '':
                preparation.append(text)

        # additional attributes
        new_recipe = ParsedRecipe(recipe.url, name, ingredients, preparation)
        attributes = {'description': soup.select('div#recipe-intronote'),
                      'serves': soup.select('span.yield'), 'cook_time': soup.select('span.cooktime'),
                      'prep_time': soup.select('span.preptime')}
        for key, value in attributes.items():
            if len(value) != 0:
                new_recipe.add_attribute(key, value[0].get_text())

        return new_recipe
