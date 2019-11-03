# -*- coding: utf-8 -*-

# Standard library imports
import argparse
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Third-party imports

# Application-specific imports
from topojson import topology


def read(specifiers):
    objs = dict()

    for specifier in specifiers:
        i = specifier.find('=')
        if 0 <= i:
            name, file = specifier.split('=')
        else:
            file = specifier
            filename = os.path.basename(file)
            name, _ = os.path.splitext(filename)

        if name in objs:
            print()
            print(f'  error: object {name} is not unique')
            print()

        else:
            objs[name] = read_object(file)

    return objs


def read_object(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return json.loads(data)


def read_newline_delimited_object():
    pass


def write(data, output):
    if isinstance(output, str):
        with open(output, 'w') as dst:
            json.dump(data, dst)
    else:
        json.dump(data, output)


if __name__ == '__main__':
    # Create OptionParser object and set options
    parser = argparse.ArgumentParser(description='Converts GeoJSON features to TopoJSON objects.')

    parser.add_argument('-o', '--out', dest='file',
                        help='output file name; defaults to “-” for stdout', default='-')
    # parser.add_argument('-n', '--newline-delimited',
    #                     help='accept newline-delimited JSON')
    parser.add_argument('-q', '--quantization', dest='count', type=float,
                        help='pre-quantization parameter; 0 disables quantization', default=0)
    parser.add_argument('geojsons', metavar='[name=]file', type=str, nargs='+',
                        help='file with GeoJSON data')

    # Parse and store the command-line arguments in dictionary
    opts = parser.parse_args()
    kwargs = vars(opts)

    # Output destination
    out = kwargs['file'] if kwargs['file'] != '-' else sys.stdout

    # Quantization
    quant = {'quantization': kwargs['count']}
    quant = quant if quant['quantization'] != 0 else dict()

    # Read files and compute topology
    objects = read(kwargs['geojsons'])
    topology = topology.Topology()
    topo = topology(objects, **quant)

    # Write TopoJSON
    write(topo, out)
