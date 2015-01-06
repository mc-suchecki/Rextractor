""" Module containing SimplyRecipesWebsite used by WebScraper. """
__author__ = "Maciej Suchecki"

import bs4
import requests
from rextractor.scraper.website import Website
from rextractor.model.recipe import RawRecipe


class SimplyRecipesWebsite(Website):
    """ Website representing http://www.simplyrecipes.com/ """

    def get_recipes(self):
        """ Fetches all of the available recipes from the website.
        :return: list of RawRecipe objects
        """
        # TODO uncomment this and delete next in order to get all recipes
        #recipes_urls = self.__get_urls()
        recipes_urls = self.__get_urls_from_first_page()

        return self.__create_recipes(recipes_urls)

    def __get_urls(self):
        """ Fetches URLs of all of the available recipes from the website.
        :return: list of recipes URLs
        """
        urls = []

        # first page has different layout
        urls += self.__get_urls_from_first_page()

        # scrape the next pages
        base_url = "http://www.simplyrecipes.com/page/"
        for url in [base_url + str(i) for i in range(2, 100)]:
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text)
            tags = soup.select('div.site-content a[href^=http://www.simplyrecipes.com/recipes/]')
            print(str(len(tags)) + " recipes found on: " + url)
            urls += [a.attrs.get('href') for a in tags]
            if self.__this_is_the_last_page(soup):
                break

        return urls

    @staticmethod
    def __this_is_the_last_page(soup):
        """ Checks if "More posts" button exists on website - stop condition. """
        return len(soup.select('div.nav-previous')) == 0

    @staticmethod
    def __get_urls_from_first_page():
        """ Gets URLs of the recipes from the first page (exists because of different layout). """
        response = requests.get("http://www.simplyrecipes.com/")
        soup = bs4.BeautifulSoup(response.text)
        tags = soup.select('div.site-content a[href^=http://www.simplyrecipes.com/recipes/]')
        urls = [a.attrs.get('href') for a in tags if 'ingredient' not in a.attrs.get('href')]
        # return urls without first 4 duplicates (featured recipe)
        return urls[4:]

    @staticmethod
    def __create_recipes(recipes_urls):
        """ Downloads recipes data from given URLs and creates RawRecipes from that.
        :param recipes_urls: URLs of the recipes
        :return: list of RawRecipe objects
        """
        recipes = []

        # iterate over URLs and get HTML code
        for url in recipes_urls:
            # little hack - add /print/ at the end to limit unnecessary downloads
            response = requests.get(url + "print/")
            soup = bs4.BeautifulSoup(response.text)
            title = str(soup.select('h1.entry-title')[0])
            recipe = str(soup.select('div.recipe-callout')[0])
            recipes.append(RawRecipe(url, title + recipe))

        return recipes

