from pathlib import Path
from rdflib import Graph, Literal, URIRef
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
    process_simple(in_dir + '/schema/*.ttl', out_dir + '/schema/schema')
    process_ontology(in_dir, out_dir)
    # TODO: also save each entity separately? for slash path access
    #  Would have to group by S, filter by those in OpenCS namespace.


def process_simple(in_glob: str, out_base_path: str, out_gzip: bool = False):
    schema = Graph()
    opencs.parse_all(schema, in_glob)
    Path(out_base_path).parent.mkdir(parents=True, exist_ok=True)
    opencs.serialize_multi(schema, out_base_path, use_gzip=out_gzip)


def process_ontology(in_dir: str, out_dir: str):
    g = Graph()
    opencs.parse_all(g, in_dir + '/ontology/core/**/*.ttl')
    g.parse(in_dir + '/ontology/header.ttl')
    # TODO: rewrite version in header
    # TODO: save the header separately as well?
    g.parse(in_dir + '/ontology/authors.ttl')
    Path(out_dir + '/ontology').mkdir(parents=True, exist_ok=True)
    opencs.serialize_multi(g, out_dir + '/ontology/ocs', use_gzip=True)


if __name__ == "__main__":
    main()
