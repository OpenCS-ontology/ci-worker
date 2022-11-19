import glob
import gzip
from rdflib import Graph, Literal, URIRef


def parse_all(g: Graph, glob_path: str):
    """
    Parse all RDF files in glob_path and add them to graph g.
    Supports reading gzip-compressed files (with .gz extension).
    :param g: graph
    :param glob_path: glob path to search files by
    :return:
    """
    i = 1
    for filename in glob.iglob(glob_path, recursive=True):
        if i % 1000 == 0:
            print(f'Parsed {i}/?? files in {glob_path}')
        if filename.endswith('.gz'):
            with gzip.open(filename, 'rt') as fp:
                g.parse(fp)
        else:
            g.parse(filename)
        i += 1


def serialize_multi(g: Graph, base_path: str, use_gzip: bool = False):
    """
    Serialize g into multiple formats.
    :param g: graph to serialize
    :param base_path: path to file to write, without the extension
    :param use_gzip: whether to use gzip compression
    :return:
    """
    formats = {
        'turtle': 'ttl',
        'nt': 'nt',
        'xml': 'xml',
    }

    for format_name, extension in formats.items():
        if use_gzip:
            with gzip.open(f'{base_path}.{extension}.gz', 'wb') as fp:
                g.serialize(fp, format=format_name)
        else:
            g.serialize(base_path + '.' + extension, format=format_name)
