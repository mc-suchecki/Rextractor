import unittest
import os.path
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
        # test with all test data from resources dir
        correct = 0
        total = 0
        i = 1
        while True:
            in_file = "resources/nlp_test%s_in.txt" % i
            if not os.path.isfile(in_file):
                break
            out_file = "resources/nlp_test%s_out.txt" % i
            result = self.__execute(in_file, out_file)
            correct += result[1]
            total += result[2]
            i += 1
        print("Total test result: correctly processed %s from %s ingredients (%s %%)" % (
            correct, total, round(100 * correct / total)))
        assert correct == total

    def __execute(self, in_filename, out_filename):
        """ Executes the NLProcessor test on data read from files
        :param in_filename: input file name
        :param out_filename: expected output file name
        :return: test result as a tuple (success, correct, all)
        """
        with open(in_filename) as in_file:
            ingredient_lines = in_file.readlines()
        with open(out_filename) as out_file:
            output_lines = out_file.readlines()
        input_parsed_recipe = ParsedRecipe("test", "test", ingredient_lines, "test")
        expected_output_ingredients = list(map(lambda line: self.parseOutFileLine(line), output_lines))
        expected_output = ProcessedRecipe("test", "test", expected_output_ingredients, "test")
        return self.__performTest(input_parsed_recipe, expected_output)

    def parseOutFileLine(self, line):
        """ Parses the expected output file line (file format: <ingredient name>\t<value>\t<unit name>)
        :param line: line
        :return: parsed result as Ingredient
        """
        elements = line.rstrip('\n').split(';', 3)
        for i in range(len(elements), 3):
            elements.append(None)
        return Ingredient(elements[0], IngredientAmount(float(elements[1]), elements[2]))

    def __performTest(self, input_parsed_recipe, expected_output):
        """ Executes the test on input_parsed_recipe and checks if the result's equal to expected_output
        :param input_parsed_recipe:
        :param expected_output:
        :return: test result as a tuple (success, correct, all)
        """
        processed_recipe = NLProcessor().process_recipe(input_parsed_recipe)
        result = processed_recipe == expected_output
        total = len(expected_output.ingredients)
        if result:
            print('Test passed')
            correct = total
        else:
            print("Test failed:\n expected:\t %s;\n actual:\t %s" % (
                expected_output.ingredients, processed_recipe.ingredients))
            correct = 0
            for i in range(min(len(expected_output.ingredients), len(processed_recipe.ingredients))):
                if expected_output.ingredients[i] == processed_recipe.ingredients[i]:
                    correct += 1
        print("Correctly processed %s from %s ingredients" % (correct, total))
        return result, correct, total


if __name__ == '__main__':
    unittest.main()