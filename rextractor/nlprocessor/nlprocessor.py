from rextractor.model.recipe import ProcessedRecipe
from rextractor.nlprocessor.extractor import IngredientExtractor

__author__ = 'Michał Toporowski'
# TODO


class NLProcessor:
    """ The natural language processing module
    """

    def process(self, parsed_recipe):
        """ Processes the ParsedRecipe containing text information to ProcessedRecipe containing object information

        :param parsed_recipe: ParsedRecipe object
        :return: ProcessedRecipe object
        """
        processed_recipe = ProcessedRecipe()
        processed_recipe.url = parsed_recipe.url
        processed_recipe.name = parsed_recipe.name
        processed_recipe.preparation = parsed_recipe.preparation
        processed_recipe.additionalAttributes = parsed_recipe.additionalAttributes
        processed_recipe.ingredients = list(map(lambda i: IngredientExtractor().extract(i), parsed_recipe.ingredients))
        return processed_recipe