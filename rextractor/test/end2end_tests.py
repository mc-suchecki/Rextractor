import difflib
import unittest
from unittest.mock import MagicMock
from rextractor.db.db import GraphDatabase
from rextractor.nlprocessor.nlprocessor import NLProcessor
from rextractor.parser.parser import HTMLParser
from rextractor.scraper.scraper import WebScraper

__author__ = 'Michał Toporowski'


class End2EndTests(unittest.TestCase):
    """ End-to-end unit tests
    """

    urls = ['http://www.simplyrecipes.com/recipes/broccoli_cheddar_mac_and_cheese/',
            'http://www.simplyrecipes.com/recipes/citrusy_cabbage_salad_with_cumin_and_coriander/']

    def setUp(self):
        self.scraper = WebScraper()
        self.parser = HTMLParser()
        self.processor = NLProcessor()
        self.database = GraphDatabase()

    def testRextractor(self):
        # Run Rextractor
        recipes = self.scraper.scrape_recipes(self.urls)
        recipes = self.parser.parse_html(recipes)
        recipes = self.processor.process(recipes)
        self.database.import_recipes(recipes)
        self.database.export_to_file('test_recipes.rdf')
        # Compare the files
        actual_lines = open("test_recipes.rdf").readlines()
        expected_lines = open("resources/recipes.rdf").readlines()
        d = difflib.Differ()
        diff = d.compare(actual_lines, expected_lines)
        result = '\n'.join(diff)
        print(result)
        assert result.strip() == ''