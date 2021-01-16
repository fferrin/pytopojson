import json
import subprocess
import unittest

from tests import in_delta


class Geo2TopoTestCase(unittest.TestCase):
    def geo2topo(self, output, options=""):
        options = " ".join(options.split()).split(" ")
        p = subprocess.run(["python", "bin/geo2topo.py", *options], capture_output=True)
        out, err = p.stdout, p.stderr
        actual = json.loads(out.decode("utf8").strip().replace("'", '"'))
        with open(output, "r") as f:
            expected = json.load(f)

        self.assertTrue(in_delta.in_delta(actual, expected))

    def test_polygons(self):
        self.geo2topo(
            "tests/server/topojson/polygon-no-quantization.json",
            "polygon=tests/server/geojson/polygon-clockwise.json",
        )

    def test_quantized_polygons(self):
        self.geo2topo(
            "tests/server/topojson/polygon.json",
            "-q 1E4 polygon=tests/server/geojson/polygon-clockwise.json",
        )

    def test_empty_geometries(self):
        self.geo2topo(
            "tests/server/topojson/empty.json",
            "multilinestring=tests/server/geojson/empty-multilinestring.json"
            " multipoint=tests/server/geojson/empty-multipoint.json"
            " multipolygon=tests/server/geojson/empty-multipolygon.json"
            " multipolygon2=tests/server/geojson/empty-multipolygon2.json"
            " polygon=tests/server/geojson/empty-polygon.json",
        )

    def test_us_map(self):
        self.geo2topo(
            "tests/client/topojson/us-states.json",
            "tests/client/geojson/us-states.json",
        )

    def test_quantized_us_map(self):
        self.geo2topo(
            "tests/client/topojson/us-states-q1e2.json",
            "-q 1E2 tests/client/geojson/us-states.json",
        )
