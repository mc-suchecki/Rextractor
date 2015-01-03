""" Module containing Website abstract base class for all Websites. """
__author__ = "Maciej Suchecki"


class Website(object):
    """ Abstract base class for every Website - defines Website interface. """
    def get_recipes(self):
        """ Extracts all of the recipes from one website.
        :return: list of RawRecipe objects
        """
        raise NotImplementedError("Please implement this method in every Website!")
