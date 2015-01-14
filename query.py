__author__ = 'Maciej Suchecki'

# TODO check this file with pylint

import sys
from rdflib import Graph
from rdflib.namespace import OWL
from rdflib.plugins.sparql import prepareQuery
from rextractor.db.namespace import RO


def initialize_graph():
    graph = Graph()
    graph.parse('recipes.rdf', format='turtle')
    return graph


def build_possible_queries():
    names = []
    queries = []
    names.append('List all imported recipes')
    queries.append(prepareQuery("""SELECT ?name WHERE { ?r owl:Class ro:Recipe . ?r ro:name ?name . }""", initNs={'ro': RO, 'owl': OWL}))
    return names, queries


def execute_query_and_print_result(query, graph):
    result = graph.query(query)
    for row in result:
        print("%s" % row)


def print_possible_queries(names):
    print('\nHere are possible queries:')
    index = 0
    for name in names:
        print(str(index) + '. ' + name)


def main():
    graph = initialize_graph()
    names, queries = build_possible_queries()

    while True:
        print_possible_queries(names)
        number = input('\nPlease input query number (blank line exits): ')
        if len(number) == 0:
            break
        print('\nExecuting query number ' + number + '...')
        number = int(number)
        execute_query_and_print_result(queries[number], graph)


if __name__ == '__main__':
    sys.exit(main())
