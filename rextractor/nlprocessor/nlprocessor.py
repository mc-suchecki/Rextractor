__author__ = 'Michał Toporowski'
from rextractor.model.recipe import ProcessedRecipe
from rextractor.nlprocessor.extractor import IngredientExtractor


class NLProcessor:
    """ The natural language processing module
    """

    def process(self, parsed_recipes):
        """ Processes the ParsedRecipes containing text information to ProcessedRecipes containing object information

        :param parsed_recipes: list of ParsedRecipe objects
        :return: list of ProcessedRecipe objects
        """
        return list(map(lambda recipe: self.process_recipe(recipe), parsed_recipes))

    def process_recipe(self, parsed_recipe):
        """ Processes the ParsedRecipe containing text information to ProcessedRecipe containing object information

        :param parsed_recipe: ParsedRecipe object
        :return: ProcessedRecipe object
        """
        ingredients = self.extract_ingredients(parsed_recipe.ingredients)
        processed_recipe = ProcessedRecipe(parsed_recipe.url, parsed_recipe.name, ingredients, parsed_recipe.preparation)
        processed_recipe.additional_attributes = parsed_recipe.additional_attributes
        return processed_recipe

    def extract_ingredients(self, ingredient_lines):
        ingredients = []
        for line in ingredient_lines:
            try:
                ingredient = IngredientExtractor().extract(line)
                ingredients.append(ingredient)
            except NameError:
                # Omit erroneous lines
                pass
        return ingredients