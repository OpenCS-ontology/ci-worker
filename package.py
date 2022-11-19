from datetime import datetime
from pathlib import Path
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, DCTERMS
import sys

import opencs


def main():
    if len(sys.argv) != 4:
        print(
            'Packages the schema and the ontology\n'
            'Args: \n'
            '- input dir – root of OpenCS repo (no trailing slash);\n'
            '- output dir (no trailing slash)\n'
            '- version tag for the ontology (not schema)'
        )
        exit(1)

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    version = sys.argv[3]
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    process_simple(in_dir + '/schema/*.ttl', out_dir + '/opencs_schema')
    process_ontology(in_dir, out_dir, version)
    # TODO: also save each entity separately? for slash path access to specific entities
    #  Would have to group by S, filter by those in OpenCS namespace.


def process_simple(in_glob: str, out_base_path: str, out_gzip: bool = False):
    schema = Graph()
    opencs.parse_all(schema, in_glob)
    Path(out_base_path).parent.mkdir(parents=True, exist_ok=True)
    opencs.serialize_multi(schema, out_base_path, use_gzip=out_gzip)


def process_ontology(in_dir: str, out_dir: str, version: str):
    g = get_auto_header(version)
    g.parse(in_dir + '/ontology/header.ttl')
    opencs.serialize_multi(g, out_dir + '/opencs_header')
    opencs.parse_all(g, in_dir + '/ontology/core/**/*.ttl')
    g.parse(in_dir + '/ontology/authors.ttl')
    opencs.serialize_multi(g, out_dir + '/opencs', use_gzip=True)


def get_auto_header(version: str) -> Graph:
    # TODO: add more stuff?
    g = Graph()
    g.bind('dcterms', DCTERMS)
    onto = URIRef('https://w3id.org/ocs/ont')
    g.add((onto, OWL.versionIRI, URIRef(onto + '/' + version)))
    g.add((onto, DCTERMS.issued, Literal(datetime.utcnow())))
    return g


if __name__ == "__main__":
    main()
