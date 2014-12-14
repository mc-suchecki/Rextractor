from rextractor.model.recipe import Ingredient, IngredientAmount


class IngredientExtractor:
    """ Class for extracting ingredients data from text
    """

    def extract(self, ingredient_text):
        """ Extracts the ingredient from ingredient_text
        :param ingredient_text:
        :return: extracted ingredient
        """
        # FIXME Mock implementation
        ingredient = Ingredient()
        ingredient.name = 'Mock'
        ingredient.amount = IngredientAmount(0, 'unit')
        return ingredient