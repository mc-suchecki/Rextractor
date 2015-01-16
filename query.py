__author__ = 'Maciej Suchecki'

# TODO check this file with pylint

import sys
from rdflib import Graph, Literal
from rdflib.namespace import OWL, XSD
from rdflib.plugins.sparql import prepareQuery
from rextractor.db.namespace import RO


class Query:
    """ Small class containing Query data. """
    def __init__(self, name, query, prompt=None):
        self.name = name
        self.query = query
        self.prompt = prompt


def initialize_graph():
    graph = Graph()
    graph.parse('recipes.rdf', format='turtle')
    return graph


def build_possible_queries():
    queries = []
    query = prepareQuery("""SELECT ?name
        WHERE { ?r owl:Class ro:Recipe .
                ?r ro:name ?name . }
        ORDER BY ?name""", initNs={'ro': RO, 'owl': OWL})
    queries.append(Query('List all imported recipes', query))
    query = prepareQuery("""SELECT ?name
        WHERE { ?i owl:Class ro:Food .
                ?i ro:food_name ?name . }
        ORDER BY ?name""", initNs={'ro': RO, 'owl': OWL})
    queries.append(Query('List all imported ingredients', query))
    query = prepareQuery("""SELECT ?name
        WHERE { ?recipe ro:name ?name .
                ?recipe ro:ingredient ?ingredient .
                ?ingredient ro:food ?food .
                ?food ro:food_name ?param . }
        ORDER BY ?name""", initNs={'ro': RO, 'owl': OWL})
    queries.append(Query('List all recipes containing desired ingredient', query, 'Ingredient name: '))
    return queries


def execute_query(query, graph, param=None):
    if param is None:
        return graph.query(query)
    return graph.query(query, initBindings={'param': Literal(param, datatype=XSD.string)})


def print_possible_queries(queries):
    print('\nHere are possible queries:')
    index = 0
    for query in queries:
        print(str(index) + '. ' + query.name)
        index += 1


def main():
    graph = initialize_graph()
    queries = build_possible_queries()

    while True:
        print_possible_queries(queries)
        number = input('\nPlease input query number (blank line exits): ')
        if len(number) == 0:
            break
        print('\nExecuting query number ' + number + '...')
        number = int(number)
        if queries[number].prompt is None:
            result = execute_query(queries[number].query, graph)
        else:
            response = input(queries[number].prompt)
            result = execute_query(queries[number].query, graph, response)
        for row in result:
            print("%s" % row)


if __name__ == '__main__':
    sys.exit(main())
