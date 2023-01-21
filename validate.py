from pyshacl import validate
from rdflib import Graph
import sys

import opencs

def main():
    if len(sys.argv) != 2:
        print(
            'Validates the ontology\n'
            'Args: \n'
            '- input dir – root of OpenCS repo (no trailing slash)'
        )
        exit(1)
    in_dir = sys.argv[1]
    process_validate_ontology(in_dir)

def process_validate_ontology(in_dir: str):
    g = Graph()
    g.parse(in_dir + '/ontology/header.ttl')
    opencs.parse_all(g, in_dir + '/ontology/core/**/*.ttl')
    g.parse(in_dir + '/ontology/authors.ttl')
    with open(in_dir + '/ontology/shacl_constraints.ttl', encoding='utf8') as f:
        shacl_text = f.read()
    validate_shacl(g, shacl_text)
    
def validate_shacl(g: Graph, shacl_text: str):
    report = validate(g,
        shacl_graph=shacl_text,
        ont_graph=None,
        inference=None,
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
        js=False,
        debug=False)
    conforms, results_graph, results_text = report
    if not conforms:
        print(results_text)
        exit(1)
    else:
        print('Validated! No issues found!') 

if __name__ == "__main__":
    main()
