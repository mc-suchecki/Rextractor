""" Module containing WebScraper class. """
__author__ = 'Maciej Suchecki'

from rextractor.scraper.websites.simply_recipes import SimplyRecipesWebsite


class WebScraper:
    """ Class responsible for scraping recipes from websites containing them. Uses Websites - which
     are predefined to suit structure of each website - to scrap all of the available data. """

    websites = [SimplyRecipesWebsite()]

    def scrape_recipes(self):
        """ Scraps recipes from every defined website.
        :return: list of RawRecipes returned from websites
        """
        recipes = []

        for website in self.websites:
            recipes += website.get_recipes()

        return recipes
