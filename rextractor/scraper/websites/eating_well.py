""" Module containing EatingWellWebsite used by WebScraper. """
__author__ = "Maciej Suchecki"

import bs4
import requests
from rextractor.scraper.website import Website
from rextractor.model.recipe import RawRecipe
from rextractor.model.websites import Websites


class EatingWellWebsite(Website):
    """ Website representing http://www.eatingwell.com/. """

    def get_recipes(self, urls=None):
        """ Fetches all of the available recipes from the website.
        :return: list of RawRecipe objects
        """
        # TODO remove this!
        if urls is not None:
            return []
        recipes_urls = self.__get_urls()
        return self.__create_recipes(recipes_urls)

    def __get_urls(self):
        """ Fetches URLs of all of the available recipes from the website.
        :return: list of recipes URLs
        """
        urls = set()

        # parse first page
        response = requests.get('http://www.eatingwell.com/recipes/browse_all_recipes')
        soup = bs4.BeautifulSoup(response.text)
        tags = soup.select('div.view-content a[href^=/recipes/]')
        urls |= set(['http://www.eatingwell.com' + a.attrs.get('href') for a in tags])

        # parse the rest
        # TODO uncomment this in order to get all recipes
        """base_url = 'http://www.eatingwell.com/recipes/browse_all_recipes?page='
        for url in [base_url + str(i) for i in range(1, 200)]:
            print('Parsing ' + url + '...')
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text)
            tags = soup.select('div.view-content a[href^=/recipes/]')
            urls |= set(['http://www.eatingwell.com' + a.attrs.get('href') for a in tags])
            if self.__this_is_the_last_page(soup):
                break"""

        return list(urls)

    @staticmethod
    def __this_is_the_last_page(soup):
        """ Checks if "last >>" link exists on website - stop condition. """
        return len(soup.select('li.pager-last')) == 0

    @staticmethod
    def __create_recipes(recipes_urls):
        """ Downloads recipes data from given URLs and creates RawRecipes from that.
        :param recipes_urls: URLs of the recipes
        :return: list of RawRecipe objects
        """
        recipes = []

        # iterate over URLs and get HTML code
        for url in recipes_urls:
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text)
            html = str(soup.select('div.content')[0])
            recipes.append(RawRecipe(url, html, Websites.EATING_WELL))

        return recipes
