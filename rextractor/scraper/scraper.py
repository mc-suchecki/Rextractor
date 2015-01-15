""" Module containing WebScraper class. """
__author__ = 'Maciej Suchecki'

from rextractor.scraper.websites.simply_recipes import SimplyRecipesWebsite


class WebScraper:
    """ Class responsible for scraping recipes from websites containing them. Uses Websites - which
     are predefined to suit structure of each website - to scrap all of the available data. """

    websites = [SimplyRecipesWebsite()]

    def scrape_recipes(self, urls=None):
        """ Scraps recipes from every defined website.
        :param urls URL addresses of recipes (if None given, they're extracted automatically)
        :return: list of RawRecipes returned from websites
        """
        recipes = []

        for website in self.websites:
            recipes += website.get_recipes(urls)

        return recipes
