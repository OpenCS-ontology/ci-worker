from functools import total_ordering
import gzip
from pathlib import Path
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import SKOS
import sys


OCS = Namespace('https://w3id.org/ocs/ont/')


@total_ordering
class ConceptIRI(URIRef):
    concept_id: int = 0

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: URIRef):
        if isinstance(other, ConceptIRI):
            return self.concept_id.__eq__(other.concept_id)
        else:
            return super().__eq__(other)

    def __gt__(self, other: URIRef):
        if isinstance(other, ConceptIRI):
            return self.concept_id.__gt__(other.concept_id)
        else:
            return super().__gt__(other)

    def __lt__(self, other: URIRef):
        if isinstance(other, ConceptIRI):
            return self.concept_id.__lt__(other.concept_id)
        else:
            return super().__lt__(other)


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
                    o = fix_o(o)
                if 'w3id.org/ocs/ont/C' in o:
                    o = ConceptIRI(str(o))
                    o.concept_id = int(o[o.rindex('/') + 2:])
            g1.add((s, p, o))

        s_str = str(s)
        c_num = int(s_str[s_str.rindex('/C') + 2:])
        dir_path = Path(f'{out_name}/{c_num // 1000:02d}')
        dir_path.mkdir(parents=True, exist_ok=True)
        g1.serialize(f'{dir_path}/C{c_num}.ttl', format='turtle')

    print('Done!')


def fix_o(o: URIRef) -> URIRef:
    if 'dbpedia.org/' not in o:
        return o
    return URIRef(o.replace('"', '%22').replace('^', '%5E'))


if __name__ == "__main__":
    main()
