import nltk
from rextractor.model.recipe import PreparationStep
from rextractor.nlprocessor.extractor import ListStemmer

__author__ = 'Michał Toporowski'


class StepAssociator:
    """ Class for associating steps with ingredients
    """

    def __init__(self, ingredients):
        self.ingredients = ingredients

    def process(self, step_text):
        """ Extracts the steps from the preparation description
        :param step_text: the preparation description
        :return: list of PreparationStep objects
        """
        step = PreparationStep()
        step.text = step_text
        stemmer = ListStemmer()
        step_words = stemmer.stem(nltk.word_tokenize(step_text))
        # We associate a step with an ingredient if its name exists in the stemmed step text
        # The spaces added, so that no word parts would be classified as words
        stemmed_text = ' ' + " ".join(step_words) + ' '
        for ing in self.ingredients:
            # We are looking only for the last word of the name (the rest are epithets, which may not appear)
            name_words = nltk.word_tokenize(ing.name)
            if name_words[-1] in stemmed_text:
                step.ingredients.append(ing)
        return step