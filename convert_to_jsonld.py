# This file includes functions used to convert
# nodes into jsonld files
# usage: convert_to_jsonld.py [-h] input_file [destination]

import os
import argparse
import json
from contextlib import contextmanager
from rdflib import Graph, SKOS


# query used to choose concepts
SELECT_CONCEPTS_QUERY = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?concept
    WHERE {
        ?concept a skos:Concept .
    }
"""


def existing_file(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"{path} does not exist.")
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"{path} is not a file.")
    return path


def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert OpenCS graph (.ttl) into single Concept files (jsonld).")
    parser.add_argument("input", help="Path to the .ttl file",
                        type=existing_file)
    parser.add_argument("destination", nargs="?", default=".", help="Destination path")
    return parser.parse_args()


@contextmanager
def change_directory(new_dir):
    """Context to change working directory, execute action,
    and change back the working directory. If new_dir does not
    exist, it is created"""
    prev_dir = os.getcwd()
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)


def get_dirname_from_concept(filename):
    """Returns the directory name in which the concept should be stored.
    Follows the same scheme for core structure of .ttl files, namely
    a directory per 1000 files"""
    concept_number = int(filename.split("C")[1])
    directory = f"{concept_number // 1000:02}"  # 1000 files per dir
    return directory


def load_graph(file, format="turtle"):
    """Loads a Graph from file in given format"""
    graph = Graph()
    graph.parse(file, format)
    return graph


def select_triples_with_query(graph: Graph, query: str):
    triples = graph.query(query)
    return triples


def save_graph_to_jsonld(graph: Graph, filepath: str):
    if not filepath.endswith(".jsonld"):
        filepath += ".jsonld"
    with open(filepath, "w", encoding="utf-8") as f:
        jsonld_data = graph.serialize(format='json-ld')
        f.write(jsonld_data)


def process_single_concept(graph, concept_uri, concept_dict):
    # get triples for particular concept (by URI)
    concept_triples = graph.triples((concept_uri, None, None))
    # create a separate "mini" graph for each concept
    concept_graph = Graph()
    for triple in concept_triples:
        concept_graph.add(triple)
    # save (prefLabel, id) in concept_dict
    conceptId = concept_uri.split('/')[-1]
    conceptPrefLabel = [str(prefLabel) for prefLabel in
                        concept_graph.objects(predicate=SKOS.prefLabel)][0]
    concept_dict[conceptPrefLabel] = conceptId
    # serialize as JSON-LD and save to file
    save_graph_to_jsonld(concept_graph, conceptId)


def process_concepts(graph, concepts, concept_dict):
    for concept in concepts:
        concept_uri = concept[0]
        with change_directory(get_dirname_from_concept(str(concept_uri))):
            process_single_concept(graph, concept_uri, concept_dict)


def main():
    concept_dict = {}  # dictionary to store (conceptId, prefLabel) for browser
    args = parse_arguments()
    openCS = load_graph(args.input)
    # serialise individual concepts as jsonld files
    with change_directory(args.destination):
        concept_triples = select_triples_with_query(openCS,
                                                    SELECT_CONCEPTS_QUERY)
        process_concepts(openCS, concept_triples, concept_dict)
    # save concept_dict
    with open("index_dict.json", "w") as file:
        json.dump(concept_dict, file)


if __name__ == "__main__":
    args = parse_arguments()
    main()
