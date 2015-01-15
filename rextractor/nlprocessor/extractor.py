__author__ = 'Michał Toporowski'
from rextractor.model.recipe import Ingredient, IngredientAmount
from nltk.stem.snowball import SnowballStemmer
import re
import nltk


class IngredientExtractor:
    """ Class for extracting ingredients data from text
    """
    __default_unit = 'item'

    def extract(self, ingredient_text):
        """ Extracts the ingredient from ingredient_text
        :param ingredient_text:
        :return: extracted ingredient
        """

        ingredient_text = Replacer().replace(ingredient_text)
        words = nltk.word_tokenize(ingredient_text)
        # Tag the parts of speech - interesting are noun clusters and numbers
        tagged_words = TaggedWords(words)
        # Refer to NLTK documentation, NN, NNS, NNPS, NNP are nouns; CD - cardinal numbers; LS - list item markers
        nouns = tagged_words.get_pos_indices(['NN'])
        numbers = tagged_words.get_pos_indices(['CD', 'LS'])
        if not numbers:
            # No numbers in text - assume 1 as amount
            value = 1.0
        else:
            number_seqs = self.extract_sequences(numbers)
            value_seq = number_seqs[0]
            value = self.parse_numbers(tagged_words.get_words(value_seq))

        noun_seqs = self.extract_sequences(nouns)
        if len(noun_seqs) < 1:
            # Error - no nouns in ingredient text
            raise NameError('Incorrect ingredient text - no nouns')
        elif len(noun_seqs) == 1:
            # Assume first noun as unit, rest as ingredient
            first_idx = noun_seqs[0][0]
            last_idx = noun_seqs[0][1]
            if first_idx == last_idx:
                # Single noun: no unit, noun is the ingredient
                unit_words = [self.__default_unit]
                name_words = tagged_words.get_words((last_idx, last_idx))
            elif numbers and first_idx - numbers[-1] > 1:
                # Multiple nouns, but there's a space between numbers and 1st noun
                # Assume no unit, all nouns as ingredient
                unit_words = [self.__default_unit]
                name_words = tagged_words.get_words((first_idx, last_idx))
            else:
                # Multiple nouns
                # Assume first noun as unit, rest as ingredient
                unit_words = tagged_words.get_words((first_idx, first_idx))
                name_words = tagged_words.get_words((first_idx + 1, last_idx))
            # Append adjectives to name_words
            name_words = tagged_words.add_all_preceding(last_idx, ['VBN', 'JJ'], name_words)
        else:
            # Multiple noun sequences - assume first sequence as unit, last as ingredient
            unit_words = tagged_words.get_words(noun_seqs[0])
            # The ingredient is the last noun sequence
            # unless there are separators before it - then we take the previous one
            # Separators: CC (and, or, etc.), ',', ';'
            separators = tagged_words.get_pos_indices(['CC', ',', ';'])
            separators = list(filter(lambda idx: noun_seqs[0][1] < idx < noun_seqs[-1][0], separators))
            # seq_nr: default: -1 (last); default if separators: 1
            seq_nr = -1
            if separators:
                seq_nr = 1
                for i in range(1, len(noun_seqs))[::-1]:
                    if noun_seqs[i][0] < separators[0]:
                        seq_nr = i
                        break
            name_words = tagged_words.get_words(noun_seqs[seq_nr])
            # Append adjectives to name_words
            name_words = tagged_words.add_all_preceding(noun_seqs[seq_nr][0], ['VBN', 'JJ'], name_words)

        # Now we have data in value, unit_words, name_words
        # We have to stem all words and make an ingredient object

        stemmer = ListStemmer()
        name_words = stemmer.stem(name_words)
        unit_words = stemmer.stem(unit_words)

        ingredient = Ingredient()
        ingredient.name = " ".join(name_words)
        ingredient.amount = IngredientAmount(value, " ".join(unit_words))
        return ingredient

    @staticmethod
    def extract_sequences(numbers):
        """ Extracts the sequences from a sorted number list
        e.g. for [1,2,5,6,7,14] the function returns [(1,2),(5,7),(14,14)]

        :param numbers: sorted number list
        :return: list of tuples containing sequences
        """
        sequences = []
        current_start = -2
        current_end = -2
        for number in numbers:
            if number - current_end > 1:
                # Start new sequence
                if current_start >= 0:
                    sequences.append((current_start, current_end))
                current_start = number
            current_end = number
        # Append last sequence
        if current_start >= 0:
            sequences.append((current_start, current_end))
        return sequences

    @staticmethod
    def parse_numbers(number_list):
        """ Converts the numbers from a list to a float
        :param number_list: list of numbers as strings
        :return: result value
        """
        value = 0
        for number_str in number_list:
            try:
                if "/" in number_str:
                    # A fraction - should be calculated
                    fraction_parts = number_str.split('/')
                    value += int(fraction_parts[0]) / int(fraction_parts[1])
                else:
                    value += float(number_str)
            except ValueError:
                # Do not increment value on parse errors
                pass
        return value


class TaggedWords:
    """ Class for performing operations on words tagged with part of speech code
    """

    def __init__(self, words):
        self.tagged_words_list = nltk.pos_tag(words)

    def get_pos_indices(self, allowed_pos_list):
        """ Gets the indices of words with certain part of speech

        :param allowed_pos_list: code prefixes of POS allowed to be included in result
        :return: list of indices
        """
        indices = []
        for idx, tagged_word in enumerate(self.tagged_words_list):
            if tagged_word[1][:2] in allowed_pos_list:
                indices.append(idx)
        return indices

    def get_words(self, idx_range):
        """ Gets the words with indices inside given range
        :param idx_range: index range as tuple (min, max)
        :return: list of words
        """
        return list(map(lambda tw: tw[0], self.tagged_words_list[idx_range[0]:idx_range[1] + 1]))

    def add_all_preceding(self, index, allowed_pos_list, word_list):
        """ Adds to a beginning of a word list all preceding words of certain part of speech
        :param index: index of a first word in word_list
        :param allowed_pos_list: codes of POS allowed to be added
        :param word_list: a word list
        :return: a word list with additional words in the beginning
        """
        for i in range(1, index)[::-1]:
            if self.tagged_words_list[i][1] in allowed_pos_list:
                word_list = [self.tagged_words_list[i][0]] + word_list
            else:
                break
        return word_list


class ListStemmer:
    """ Word lists stemmer
    """
    stemmer = SnowballStemmer("english")

    def stem(self, word_list):
        """ Stems a list of words
        :param word_list: words list
        :return: stemmed words list
        """
        return list(map(lambda word: self.stemmer.stem(word), word_list))


class Replacer:
    """ Class for replacing known char sequences in strings
    """
    known_fixes_dict = {
        '½': ' 1/2',
        'half': ' 1/2',
        'quarter': ' 1/4',
        ' lbs ': ' lb ',
        '-': ' ',
        ' piece ': ' '
    }

    def replace(self, string):
        """ Replaces all occurences of known char sequences in given string
        :param string: a string
        :return: string
        """
        string = string.lower()
        # Replace the sequences from dictionary
        for entry in self.known_fixes_dict.items():
            string = string.replace(entry[0], entry[1])
        # Get rid of all information in parentheses - so far we assume it's not relevant
        string = re.sub("\(.*?\)", ";", string)
        return string