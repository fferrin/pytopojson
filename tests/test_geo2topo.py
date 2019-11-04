# -*- coding: utf-8 -*-

# Standard library imports
import json
import subprocess
import unittest

# Third-party imports

# Application-specific imports
from tests import in_delta


class Geo2TopoTestCase(unittest.TestCase):
    def geo2topo(self, output, options=''):
        options = ' '.join(options.split()).split(' ')
        p = subprocess.run(['python', 'bin/geo2topo.py', *options],
                           capture_output=True)
        out, err = p.stdout, p.stderr
        actual = json.loads(out.decode('utf8').strip().replace("'", '"'))
        with open(output, 'r') as f:
            expected = json.load(f)

        self.assertTrue(in_delta.in_delta(actual, expected))

    def test_polygons(self):
        self.geo2topo('tests/topojson/polygon-no-quantization.json',
                      'polygon=tests/geojson/polygon-clockwise.json')

    def test_quantized_polygons(self):
        self.geo2topo('tests/topojson/polygon.json',
                      '-q 1E4 polygon=tests/geojson/polygon-clockwise.json')

    def test_empty_geometries(self):
        self.geo2topo('tests/topojson/empty.json',
                      'multilinestring=tests/geojson/empty-multilinestring.json'
                      ' multipoint=tests/geojson/empty-multipoint.json'
                      ' multipolygon=tests/geojson/empty-multipolygon.json'
                      ' multipolygon2=tests/geojson/empty-multipolygon2.json'
                      ' polygon=tests/geojson/empty-polygon.json')
