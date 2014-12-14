import unittest
from rextractor.model.recipe import ParsedRecipe, ProcessedRecipe, Ingredient, IngredientAmount
from rextractor.nlprocessor.nlprocessor import NLProcessor


class NLProcessorTest(unittest.TestCase):
    """ NLProcessor module unit tests
    """
    __author__ = 'Michał Toporowski'

    def testNLProcessor(self):
        """ Performs the NLProcessor module tests
        :return: nothing
        """
        # TODO:: add more test data
        self.__execute('resources/nlp_test1_in.txt', 'resources/nlp_test1_out.txt')

    def __execute(self, in_filename, out_filename):
        """ Executes the NLProcessor test on data read from files
        :param in_filename: input file name
        :param out_filename: expected output file name
        :return: nothing
        """
        with open(in_filename) as in_file:
            ingredient_lines = in_file.readlines()
        with open(out_filename) as out_file:
            output_lines = out_file.readlines()
        input_parsed_recipe = ParsedRecipe()
        input_parsed_recipe.ingredients = ingredient_lines
        expected_output = ProcessedRecipe()
        expected_output.ingredients = list(map(lambda line: self.parseOutFileLine(line), output_lines))
        self.__performTest(input_parsed_recipe, expected_output)

    def parseOutFileLine(self, line):
        """ Parses the expected output file line (file format: <ingredient name>\t<value>\t<unit name>)
        :param line: line
        :return: parsed result as Ingredient
        """
        elements = line.rstrip('\n').split('\t', 3)
        for i in range(len(elements), 3):
            elements.append(None)
        return Ingredient(elements[0], IngredientAmount(elements[1], elements[2]))

    def __performTest(self, input_parsed_recipe, expected_output):
        """ Executes the test on input_parsed_recipe and checks if the result's equal to expected_output
        :param input_parsed_recipe:
        :param expected_output:
        :return:
        """
        processed_recipe = NLProcessor().process(input_parsed_recipe)
        result = processed_recipe == expected_output
        if result:
            print('Test passed')
        else:
            print("Test failed:\n expected: %s;\n actual: %s" % (
                expected_output.ingredients, processed_recipe.ingredients))
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()