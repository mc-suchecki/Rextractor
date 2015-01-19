import difflib
import unittest
from unittest.mock import MagicMock
from rdflib import OWL, Literal, XSD
from rextractor.db.db import GraphDatabase
from rextractor.db.namespace import RO
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
        # Query the database for saved recipes
        saved_recipes = self.queryResultAsSet("""SELECT ?name
        WHERE { ?r owl:Class ro:Recipe .
                ?r ro:name ?name . }
        ORDER BY ?name""")
        expected_recipes = {'Broccoli Cheddar Mac and Cheese', 'Citrusy Cabbage Salad with Cumin and Coriander'}
        assert saved_recipes == expected_recipes
        # Query for first recipe ingredients
        cheddar_mac_ingredients = self.queryResultAsSet("""SELECT ?name
        WHERE { ?recipe ro:name ?param .
                ?recipe ro:ingredient ?ingredient .
                ?ingredient ro:food ?food .
                ?food ro:food_name ?name . }
        ORDER BY ?name""", 'Broccoli Cheddar Mac and Cheese')
        assert len(cheddar_mac_ingredients) == 13
        assert 'parmesan chees' in cheddar_mac_ingredients
        assert 'paprika' in cheddar_mac_ingredients
        assert 'grate sharp cheddar chees' in cheddar_mac_ingredients
        assert 'salt' in cheddar_mac_ingredients

    def queryResultAsSet(self, query, param=None):
        """ Returns the database query result as string set
        :param query: database query
        :param param: query parameter
        :return: result as set of strings
        """
        if param is None:
            query_result = self.database.graph.query(query, initNs={'ro': RO, 'owl': OWL})
        else:
            query_result = self.database.graph.query(query, initNs={'ro': RO, 'owl': OWL},
                                                     initBindings={'param': Literal(param, datatype=XSD.string)})
        return set(map(lambda r: str(r[0]), query_result))