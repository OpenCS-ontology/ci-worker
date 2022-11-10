import glob
from pathlib import Path
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import SKOS
import re
import sys


mw_repl = {
    '|': '{{!}}',
    '=': '{{=}}',
    '{': '{{(}}',
    '}': '{{)}}',
    '[': '{{!(}}',
    ']': '{{!)}}',
}


def main():
    if len(sys.argv) != 3:
        print(
            'Args: \n'
            '- input dir (no trailing slash);\n'
            '- output dir (no trailing slash)'
        )
        exit(1)

    in_name = sys.argv[1]
    out_name = sys.argv[2]
    for filename in glob.iglob(in_name + '/**/*.ttl', recursive=True):
        g = Graph()
        g.parse(filename)
        data = {
            'prefLabel': make_templ_arg(g, SKOS.prefLabel, '^%^'),
            'altLabel': make_templ_arg(g, SKOS.altLabel, '^%^'),
            'broader': make_templ_arg(g, SKOS.broader, map_iris=True),
            'related': make_templ_arg(g, SKOS.related, map_iris=True),
            'closeMatch': make_templ_arg(g, SKOS.closeMatch, '^%^'),
        }

        mw_filename = Path(filename.replace(in_name, out_name).replace('.ttl', '.mw'))
        mw_filename.parent.mkdir(parents=True, exist_ok=True)
        with open(mw_filename, 'wt') as fp:
            fp.write('{{Concept\n')
            for k, v in data.items():
                fp.write(f'|{k}={v}\n')
            fp.write('}}\n')


def make_templ_arg(g: Graph, p: URIRef, sep: str = ',', map_iris: bool = False) -> str:
    objects = [
        str(o) + '@' + (o.language or 'en') if isinstance(o, Literal) else str(o)
        for o in g.objects(None, p)
    ]
    if map_iris:
        objects = ['OpenCS:' + o[o.rindex('/') + 1:] for o in objects]

    value = sep.join(objects)
    value = re.sub(
        r'=\{}\|\[]',
        lambda m: mw_repl[m.group(0)],
        value
    )
    return value


if __name__ == "__main__":
    main()
