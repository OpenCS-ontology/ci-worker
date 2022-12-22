import gzip
from pathlib import Path
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import SKOS
import sys

from opencs import ConceptIRI

OCS = Namespace('https://w3id.org/ocs/ont/')


def main():
    if len(sys.argv) != 4:
        print(
            'Args: \n'
            '- input file;\n'
            '- output dir (no trailing slash);\n'
            '- whether to fix DBpedia IRIs (0/1)'
        )
        exit(1)

    in_name = sys.argv[1]
    out_name = sys.argv[2]
    fix_dbpedia = sys.argv[3] == '1'

    g = Graph()
    print('Parsing input graph...')
    if in_name.endswith('.gz'):
        with gzip.open(in_name, 'rt') as f_in:
            g.parse(f_in)
    else:
        with open(in_name, 'rt') as f_in:
            g.parse(f_in)

    i = 0
    for s in g.subjects(unique=True):
        if i % 1000 == 0:
            print(f'Saving {i}...')
        i += 1
        g1 = Graph()
        g1.bind('ocs', OCS)
        g1.bind('skos', SKOS)
        for p, o in g.predicate_objects(s):
            if isinstance(o, URIRef):
                if fix_dbpedia:
                    o = fix_o_dbpedia(o)
                if 'w3id.org/ocs/ont/C' in o:
                    o = ConceptIRI(str(o))
                    o.concept_id = int(o[o.rindex('/') + 2:])
            elif isinstance(o, Literal):
                if p == SKOS.prefLabel:
                    o = fix_o_label(o)
            g1.add((s, p, o))

        s_str = str(s)
        c_num = int(s_str[s_str.rindex('/C') + 2:])
        dir_path = Path(f'{out_name}/{c_num // 1000:02d}')
        dir_path.mkdir(parents=True, exist_ok=True)
        g1.serialize(f'{dir_path}/C{c_num}.ttl', format='turtle')

    print('Done!')


def fix_o_dbpedia(o: URIRef) -> URIRef:
    if 'dbpedia.org/' not in o:
        return o
    return URIRef(
        o.replace('"', '%22')
         .replace('^', '%5E')
         .replace('%_', '%25_')
    )


def fix_o_label(o: Literal) -> Literal:
    if o.language is None:
        return Literal(o.value, 'en')
    return o


if __name__ == "__main__":
    main()
