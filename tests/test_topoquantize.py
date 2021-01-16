import json
import subprocess
import unittest


class TopoQuantizeTestCase(unittest.TestCase):
    def topoquantize(self, command, result):
        command = " ".join(command.split()).split(" ")
        p = subprocess.run(
            ["python", "bin/topoquantize.py", *command], capture_output=True
        )
        out, err = p.stdout, p.stderr
        actual = json.loads(out)
        with open(result, "r") as f:
            expected = json.load(f)

        self.assertDictEqual(actual, expected)

    def test_polygon_quantization(self):
        # self.topoquantize('-q 1e4 < tests/client/topojson/polygon.json',
        self.topoquantize(
            "-q 1e4 -i tests/client/topojson/polygon.json",
            "tests/client/topojson/polygon-q1e4.json",
        )

    def test_polygon_quantization_2(self):
        # self.topoquantize('-q 1e5 < tests/client/topojson/polygon.json',
        self.topoquantize(
            "-q 1e5 -i tests/client/topojson/polygon.json",
            "tests/client/topojson/polygon-q1e5.json",
        )

    def test_polygon_mercator_quantization(self):
        # self.topoquantize('-q 1e4 < tests/client/topojson/polygon-mercator.json',
        self.topoquantize(
            "-q 1e4 -i tests/client/topojson/polygon-mercator.json",
            "tests/client/topojson/polygon-mercator-q1e4.json",
        )

    def test_polygon_mercator_quantization_2(self):
        # self.topoquantize('-q 1e5 < tests/client/topojson/polygon-mercator.json',
        self.topoquantize(
            "-q 1e5 -i tests/client/topojson/polygon-mercator.json",
            "tests/client/topojson/polygon-mercator-q1e5.json",
        )

    def test_point_quantization(self):
        # self.topoquantize('-q 1e5 < tests/client/topojson/point.json',
        self.topoquantize(
            "-q 1e5 -i tests/client/topojson/point.json",
            "tests/client/topojson/point-q1e5.json",
        )

    def test_points_quantization(self):
        # self.topoquantize('-q 1e5 < tests/client/topojson/points.json',
        self.topoquantize(
            "-q 1e5 -i tests/client/topojson/points.json",
            "tests/client/topojson/points-q1e5.json",
        )
