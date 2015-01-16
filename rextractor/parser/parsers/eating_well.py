__author__ = 'Maciej Suchecki'

# TODO check this file with pylint

from bs4 import BeautifulSoup
from rextractor.model.recipe import ParsedRecipe


class EatingWellParser():

    @staticmethod
    def parse_recipe(recipe):
        """ Parses HTML from one RawRecipe and converts it to ParsedRecipe.
        :param recipe: any RawRecipe with type EATING_WELL
        :return: ParsedRecipe created from given recipe
        """
        soup = BeautifulSoup(recipe.html)

        name = str(soup.select('h1[itemprop=name]')[0].string)

        ingredients = []
        for li in soup.select('li[itemprop=ingredients]'):
            text = li.get_text()
            if text != '':
                ingredients.append(text)

        preparation = []
        for li in soup.select('ol[itemprop=recipeinstructions] li'):
            text = li.get_text().strip()
            if text != '':
                preparation.append(text)

        # additional attributes
        new_recipe = ParsedRecipe(recipe.url, name, ingredients, preparation)
        attributes = {'description': soup.select('p[itemprop=description]'),
                      'serves': soup.select('span[itemprop=recipeyield]')}
        for key, value in attributes.items():
            if len(value) != 0:
                new_recipe.add_attribute(key, value[0].get_text())

        return new_recipe
