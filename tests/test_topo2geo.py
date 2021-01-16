import json
import subprocess
import unittest

from tests import in_delta


class Topo2GeoTestCase(unittest.TestCase):
    def topo2geo(self, command, result):
        command = " ".join(command.split()).split(" ")
        p = subprocess.run(["python", "bin/topo2geo.py", *command], capture_output=True)
        out, err = p.stdout, p.stderr
        actual = json.loads(out)
        with open(result, "r") as f:
            expected = json.load(f)

        self.assertTrue(in_delta.in_delta(actual, expected))

    def test_polygon(self):
        # self.topo2geo('polygon=- < tests/client/topojson/polygon.json',
        self.topo2geo(
            "polygon=- -i tests/client/topojson/polygon.json",
            "tests/client/geojson/polygon.json",
        )

    def test_polygon_quantized(self):
        # self.topo2geo('polygon=- < tests/client/topojson/polygon-q1e4.json',
        self.topo2geo(
            "polygon=- -i tests/client/topojson/polygon-q1e4.json",
            "tests/client/geojson/polygon.json",
        )

    def test_polygon_quantized_2(self):
        # self.topo2geo('polygon=- < tests/client/topojson/polygon-q1e5.json',
        self.topo2geo(
            "polygon=- -i tests/client/topojson/polygon-q1e5.json",
            "tests/client/geojson/polygon.json",
        )

    def test_polygon_mercator(self):
        # self.topo2geo('polygon=- < tests/client/topojson/polygon-mercator.json',
        self.topo2geo(
            "polygon=- -i tests/client/topojson/polygon-mercator.json",
            "tests/client/geojson/polygon-mercator.json",
        )

    def test_polygon_mercator_quantized(self):
        # self.topo2geo('polygon=- < tests/client/topojson/polygon-mercator-q1e4.json',
        self.topo2geo(
            "polygon=- -i tests/client/topojson/polygon-mercator-q1e4.json",
            "tests/client/geojson/polygon-mercator.json",
        )

    def test_polygon_mercator_quantized_2(self):
        # self.topo2geo('polygon=- < tests/client/topojson/polygon-mercator-q1e5.json',
        self.topo2geo(
            "polygon=- -i tests/client/topojson/polygon-mercator-q1e5.json",
            "tests/client/geojson/polygon-mercator.json",
        )

    # def test_polygon_united_states(self):
    #     # self.topo2geo('polygon=- < tests/client/topojson/polygon-mercator-q1e5.json',
    #     self.topo2geo(
    #         "us-states=- -i tests/client/topojson/us-states.json",
    #         "tests/client/geojson/us-states.json",
    #     )
