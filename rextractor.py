""" This is the main module of Rextractor - simple Python application extracting cooking
recipes from various websites, parsing them and storing the data in a graph database. """
__author__ = 'Maciej Suchecki'

import sys
#from rextractor.scraper.scraper import WebScraper
#from rextractor.parser.parser import HTMLParser
#from rextractor.nlprocessor.nlprocessor import NLProcessor
#from rextractor.db.db import GraphDatabase


def main():
    """ Main function of Rextractor application. """
    # scrape the recipes from selected websites
    #scraper = WebScraper()
    #recipes = scraper.scrape_websites()

    # parse the recipes to extract data from HTML
    #parser = HTMLParser()
    #recipes = parser.parse_html(recipes)

    # process the recipes using NLP to unify the language
    #processor = NLProcessor()
    #recipes = processor.process(recipes)

    # import the resulting recipes to graph database
    #database = GraphDatabase()
    #database.import_recipes(recipes)
    pass

if __name__ == '__main__':
    sys.exit(main())
