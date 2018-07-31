import unittest

from topojson import bounds, cut, delta, extract, geometry, prequantize


class BoundsTestCase(unittest.TestCase):

    def test_bounds_computes_bounding_box(self):
        foo = {
            'bar': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [0, 2], [0, 0]]
            }
        }

        self.assertListEqual(bounds.BoundingBox(foo).value, [0, 0, 1, 2])

    def test_bounds_considers_points_as_well_as_arcs(self):
        foo = {
            'bar': {
                'type': 'MultiPoint',
                'coordinates': [[0, 0], [1, 0], [0, 2], [0, 0]]
            }
        }

        self.assertListEqual(bounds.BoundingBox(foo).value, [0, 0, 1, 2])


class CutTestCase(unittest.TestCase):

    def test_cut_exact_duplicate_lines_ABC_and_ABC_have_no_cuts(self):
        e = extract.Extract({
            'abc': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [2, 0]]
            },
            'abc2': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [2, 0]]
            }
        })

        c = cut.Cut(e.value)

        self.assertDictEqual({
            'abc': {
                'type': 'LineString',
                'arcs': {
                    0: 0,
                    1: 2
                }
            },
            'abc2': {
                'type': 'LineString',
                'arcs': {
                    0: 3,
                    1: 5
                }
            }
        },
        c.value)


class DeltaTestCase(unittest.TestCase):

    def test_delta_converts_arcs_to_delta_encoding(self):
        d = delta.Delta([
            [[0, 0], [9999, 0], [0, 9999], [0, 0]]
        ])

        self.assertListEqual(
            d.arcs,
            [
                [[0, 0], [9999, 0], [-9999, 9999], [0, -9999]]
            ]
        )

    def test_delta_skips_coincident_points(self):
        d = delta.Delta([
            [[0, 0], [9999, 0], [9999, 0], [0, 9999], [0, 0]]
        ])

        self.assertListEqual(
            d.arcs,
            [
                [[0, 0], [9999, 0], [-9999, 9999], [0, -9999]]
            ]
        )

    def test_delta_preserves_at_least_two_positions(self):
        d = delta.Delta([
            [[12345, 12345], [12345, 12345], [12345, 12345], [12345, 12345]]
        ])

        self.assertListEqual(
            d.arcs,
            [
                [[12345, 12345], [0, 0]]
            ]
        )



class ExtractTestCase(unittest.TestCase):

    def test_extract_copies_coordinates_sequentially_into_a_buffer(self):
        topology = extract.Extract({
            'foo': {
                'type': "LineString",
                'arcs': [[0, 0], [1, 0], [2, 0]]
            },
            'bar': {
                'type': "LineString",
                'arcs': [[0, 0], [1, 0], [2, 0]]
            }
        })

        self.assertListEqual(topology.value['coordinates'], [[0, 0], [1, 0], [2, 0], [0, 0], [1, 0], [2, 0]])

    def test_extract_does_not_copy_point_geometries_into_the_coordinate_buffer(self):
        topology = extract.Extract({
            'foo': {
                'type': 'Point',
                'arcs': [0, 0]
            },
            'bar': {
                'type': 'MultiPoint',
                'arcs': [[0, 0], [1, 0], [2, 0]]
            }
        })

        self.assertListEqual(topology.value['coordinates'], [])
        self.assertListEqual(topology.value['objects']['foo']['arcs'], [0, 0])
        self.assertListEqual(topology.value['objects']['bar']['arcs'], [[0, 0], [1, 0], [2, 0]])

    def test_extract_includes_closing_coordinates_in_polygons(self):
        topology = extract.Extract({
            'foo': {
                'type': 'Polygon',
                'arcs': [[[0, 0], [1, 0], [2, 0], [0, 0]]]
            }
        })

        self.assertListEqual(topology.value['coordinates'], [[0, 0], [1, 0], [2, 0], [0, 0]])

    def test_extract_represents_lines_as_contiguous_slices_of_the_coordinate_buffer(self):
        topology = extract.Extract({
            'foo': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [2, 0]]
            },
            'bar': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [2, 0]]
            }
        })

        self.assertDictEqual(
            topology.value['objects'],
            {
                'foo': {
                    'type': 'LineString',
                    'arcs': [0, 2]
                },
                'bar': {
                    'type': 'LineString',
                    'arcs': [3, 5]
                }
            }
        )

    def test_extract_represents_rings_as_contiguous_slices_of_the_coordinate_buffer(self):
        topology = extract.Extract({
            'foo': {
                'type': 'Polygon',
                'arcs': [[[0, 0], [1, 0], [2, 0], [0, 0]]]
            },
            'bar': {
                'type': 'Polygon',
                'arcs': [[[0, 0], [1, 0], [2, 0], [0, 0]]]
            }
        })

        self.assertDictEqual(
            topology.value['objects'],
            {
                'foo': {
                    'type': 'Polygon',
                    'arcs': [[0, 3]]
                },
                'bar': {
                    'type': 'Polygon',
                    'arcs': [[4, 7]]
                }
            }
        )

    def test_extract_exposes_the_constructed_lines_and_rings_in_the_order_of_construction(self):
        topology = extract.Extract({
            'line': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [2, 0]]
            },
            'multiline': {
                'type': 'MultiLineString',
                'arcs': [[[0, 0], [1, 0], [2, 0]]]
            },
            'polygon': {
                'type': 'Polygon',
                'arcs': [[[0, 0], [1, 0], [2, 0], [0, 0]]]
            }
        })

        self.assertListEqual(topology.value['lines'], [[0, 2], [3, 5]])
        self.assertListEqual(topology.value['rings'], [[6, 9]])

    def test_extract_supports_nested_geometry_collections(self):
        topology = extract.Extract({
            'foo': {
                'type': 'GeometryCollection',
                'geometries': [{
                    'type': 'GeometryCollection',
                    'geometries': [{
                        'type': 'LineString',
                        'arcs': [[0, 0], [0, 1]]
                    }]
                }]
            }
        })

        self.assertDictEqual(
            topology.value['objects']['foo'],
            {
                'type': 'GeometryCollection',
                'geometries': [{
                    'type': 'GeometryCollection',
                    'geometries': [{
                        'type': 'LineString',
                        'arcs': [0, 1]
                    }]
                }]
            }

        )


class GeometryTestCase(unittest.TestCase):

    def test_geometry_replaces_LineString_Feature_with_LineString_Geometry(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [[0, 0]]
                }
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'LineString',
                    'arcs': [[0, 0]]
                }
            }
        )

    def test_geometry_replaces_GeometryCollection_Feature_with_GeometryCollection(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'Feature',
                'geometry': {
                    'type': 'GeometryCollection',
                    'geometries': [{
                        'type': 'LineString',
                        'coordinates': [[0, 0]]
                    }]
                }
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'GeometryCollection',
                    'geometries': [{
                        'type': 'LineString',
                        'arcs': [[0, 0]]
                    }]
                }
            }
        )

    def test_geometry_replaces_FeatureCollection_with_GeometryCollection(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': [[0, 0]]
                    }
                }]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'GeometryCollection',
                    'geometries': [{
                        'type': 'LineString',
                        'arcs': [[0, 0]]
                    }]
                }
            }
        )

    def test_geometry_replaces_Feature_with_null_Geometry_with_null_type_Geometry(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'Feature',
                'geometry': None
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': None
                }
            }
        )

    def test_geometry_replaces_top_level_null_Geometry_with_null_type_Geometry(self):
        geom = geometry.Geometry({
            'foo': None
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': None
                }
            }
        )

    def test_geometry_replaces_null_Geometry_in_GeometryCollection_with_null_type_Geometry(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'GeometryCollection',
                'geometries': [None]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'GeometryCollection',
                    'geometries': [{
                        'type': None
                    }]
                }
            }
        )

    def test_geometry_preserves_id(self):
        geom = geometry.Geometry({
            'foo': {
                'id': 'foo',
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [[0, 0]]
                }
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'id': 'foo',
                    'type': 'LineString',
                    'arcs': [[0, 0]]
                }
            }
        )

    def test_geometry_preserves_properties_if_non_empty(self):
        geom = geometry.Geometry({
            'foo': {
                'properties': {
                    'foo': 42
                },
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [[0, 0]]
                }
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'properties': {
                        'foo': 42
                    },
                    'type': 'LineString',
                    'arcs': [[0, 0]]
                }
            }
        )

    def test_geometry_applies_a_shallow_copy_for_properties(self):
        input = {
            'foo': {
                'properties': {
                    'foo': 42
                },
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [[0, 0]]
                }
            }
        }

        geom = geometry.Geometry(input)

        self.assertDictEqual(input['foo']['properties'], geom.output['foo']['properties'])

    def test_geometry_deletes_empty_properties(self):
        geom = geometry.Geometry({
            'foo': {
                'properties': {},
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [[0, 0]]
                }
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'LineString',
                    'arcs': [[0, 0]]
                }
            }
        )

    def test_geometry_does_not_convert_singular_multipoints_to_points(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'MultiPoint',
                'coordinates': [[0, 0]]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'MultiPoint',
                    'coordinates': [[0, 0]]
                }
            }
        )

    def test_geometry_does_not_convert_empty_multipoints_to_null(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'MultiPoint',
                'coordinates': []
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'MultiPoint',
                    'coordinates': []
                }
            }
        )

    def test_geometry_does_not_convert_singular_multilines_to_line(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'MultiLineString',
                'coordinates': [[[0, 0], [0, 1]]]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'MultiLineString',
                    'arcs': [[[0, 0], [0, 1]]]
                }
            }
        )

    def test_geometry_does_not_convert_empty_lines_to_null(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'LineString',
                'coordinates': []
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'LineString',
                    'arcs': []
                }
            }
        )

    def test_geometry_does_not_convert_empty_multilines_to_null(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'MultiLineString',
                'coordinates': []
            },
            'bar': {
                'type': 'MultiLineString',
                'coordinates': [[]]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'MultiLineString',
                    'arcs': []
                },
                'bar': {
                    'type': 'MultiLineString',
                    'arcs': [[]]
                }
            }
        )

    def test_geometry_does_not_strip_empty_lines_in_multilines(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'MultiLineString',
                'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 0]], [], [[0, 0], [1, 0]]]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'MultiLineString',
                    'arcs': [[[0, 0], [1, 0], [1, 1], [0, 0]], [], [[0, 0], [1, 0]]]
                }
            }
        )

    def test_geometry_does_not_convert_empty_polygons_to_null(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'Polygon',
                'coordinates': []
            },
            'bar': {
                'type': 'Polygon',
                'coordinates': [[]]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'Polygon',
                    'arcs': []
                },
                'bar': {
                    'type': 'Polygon',
                    'arcs': [[]]
                }
            }
        )

    def test_geometry_does_not_strip_empty_polygons_in_multipolygons(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'MultiPolygon',
                'coordinates': [[[[0, 0], [1, 0], [1, 1], [0, 0]], []], [], [[]]]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'MultiPolygon',
                    'arcs': [[[[0, 0], [1, 0], [1, 1], [0, 0]], []], [], [[]]]
                }
            }
        )

    def test_geometry_does_not_convert_singular_multipolygons_to_polygons(self):
        geom = geometry.Geometry({
            'foo': {
                'type': 'MultiPolygon',
                'coordinates': [[[[0, 0], [0, 1], [1, 0], [0, 0]]]]
            }
        })

        self.assertDictEqual(
            geom.output,
            {
                'foo': {
                    'type': 'MultiPolygon',
                    'arcs': [[[[0, 0], [0, 1], [1, 0], [0, 0]]]]
                }
            }
        )


class PrequantizeTestCase(unittest.TestCase):

    def test_prequantize_returns_the_quantization_transform(self):
        quantize = prequantize.Prequantize({}, [0, 0, 1, 1], 1e4)

        self.assertDictEqual(
            quantize.value,
            {
                'scale': [1 / 9999, 1 / 9999],
                'translate': [0, 0]
            }
        )

    def test_prequantize_converts_coordinates_to_fixed_precision(self):
        objects = {
            'foo': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [0, 1], [0, 0]]
            }
        }

        prequantize.Prequantize(objects, [0, 0, 1, 1], 1e4)
        self.assertListEqual(objects['foo']['arcs'], [[0, 0], [9999, 0], [0, 9999], [0, 0]])

    def test_prequantize_observes_the_quantization_parameter(self):
        objects = {
            'foo': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [0, 1], [0, 0]]
            }
        }

        prequantize.Prequantize(objects, [0, 0, 1, 1], 10)
        self.assertListEqual(objects['foo']['arcs'], [[0, 0], [9, 0], [0, 9], [0, 0]])

    def test_prequantize_observes_the_bounding_box(self):
        objects = {
            'foo': {
                'type': 'LineString',
                'arcs': [[0, 0], [1, 0], [0, 1], [0, 0]]
            }
        }

        prequantize.Prequantize(objects, [-1, -1, 2, 2], 10)
        self.assertListEqual(objects['foo']['arcs'], [[3, 3], [6, 3], [3, 6], [3, 3]])

    def test_prequantize_applies_to_points_as_well_as_arcs(self):
        objects = {
            'foo': {
                'type': 'MultiPoint',
                'coordinates': [[0, 0], [1, 0], [0, 1], [0, 0]]
            }
        }

        prequantize.Prequantize(objects, [0, 0, 1, 1], 1e4)
        self.assertListEqual(objects['foo']['coordinates'], [[0, 0], [9999, 0], [0, 9999], [0, 0]])

    def test_prequantize_skips_coincident_points_in_line(self):
        objects = {
            'foo': {
                'type': 'LineString',
                'arcs': [[0, 0], [0.9, 0.9], [1.1, 1.1], [2, 2]]
            }
        }

        prequantize.Prequantize(objects, [0, 0, 2, 2], 3)
        self.assertListEqual(objects['foo']['arcs'], [[0, 0], [1, 1], [2, 2]])

    def test_prequantize_skips_coincident_points_in_polygon(self):
        objects = {
            'foo': {
                'type': 'Polygon',
                'arcs': [[[0, 0], [0.9, 0.9], [1.1, 1.1], [2, 2], [0, 0]]]
            }
        }

        prequantize.Prequantize(objects, [0, 0, 2, 2], 3)
        self.assertListEqual(objects['foo']['arcs'], [[[0, 0], [1, 1], [2, 2], [0, 0]]])

    def test_prequantize_does_not_skip_coincident_points_in_point(self):
        objects = {
            'foo': {
                'type': 'MultiPoint',
                'coordinates': [[0, 0], [0.9, 0.9], [1.1, 1.1], [2, 2], [0, 0]]
            }
        }

        prequantize.Prequantize(objects, [0, 0, 2, 2], 3)
        self.assertListEqual(objects['foo']['coordinates'], [[0, 0], [1, 1], [1, 1], [2, 2], [0, 0]])

    def test_prequantize_includes_closing_point_in_degenerate_lines(self):
        objects = {
            'foo': {
                'type': 'LineString',
                'arcs': [[1, 1], [1, 1], [1, 1]]
            }
        }

        prequantize.Prequantize(objects, [0, 0, 2, 2], 3)
        self.assertListEqual(objects['foo']['arcs'], [[1, 1], [1, 1]])

    def test_prequantize_includes_closing_point_in_degenerate_polygons(self):
        objects = {
            'foo': {
                'type': 'Polygon',
                'arcs': [[[0.9, 1], [1.1, 1], [1.01, 1], [0.9, 1]]]
            }
        }

        prequantize.Prequantize(objects, [0, 0, 2, 2], 3)
        self.assertListEqual(objects['foo']['arcs'], [[[1, 1], [1, 1], [1, 1], [1, 1]]])


if __name__ == '__main__':
    unittest.main()
