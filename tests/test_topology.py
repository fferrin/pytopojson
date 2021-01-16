import unittest

from pytopojson import topology


class TopologyTestCase(unittest.TestCase):
    def setUp(self):
        self.topology = topology.Topology()

    def test_topology_exact_duplicate_lines_abc_abc_share_the_arc_abc(self):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 0],
                "arcs": [[[0, 0], [1, 0], [2, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0]},
                    "bar": {"type": "LineString", "arcs": [0]},
                },
            },
            topology,
        )

    def test_topology_reversed_duplicate_lines_abc_cba_share_the_arc_abc(self):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[2, 0], [1, 0], [0, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 0],
                "arcs": [[[0, 0], [1, 0], [2, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0]},
                    "bar": {"type": "LineString", "arcs": [~0]},
                },
            },
            topology,
        )

    def test_topology_when_old_arc_abc_extends_a_new_arc_ab_they_share_the_arc_ab(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 0], [1, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 0],
                "arcs": [[[0, 0], [1, 0]], [[1, 0], [2, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [0]},
                },
            },
            topology,
        )

    def test_topology_when_a_reversed_old_arc_cba_extends_a_new_arc_ab_they_share_the_arc_ba(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[2, 0], [1, 0], [0, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 0], [1, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 0],
                "arcs": [[[2, 0], [1, 0]], [[1, 0], [0, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [~1]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_ade_shares_its_start_with_an_old_arc_abc_they_dont_share_arcs(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 0], [1, 1], [2, 1]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 1],
                "arcs": [[[0, 0], [1, 0], [2, 0]], [[0, 0], [1, 1], [2, 1]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0]},
                    "bar": {"type": "LineString", "arcs": [1]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_dec_shares_its_start_with_an_old_arc_abc_they_dont_share_arcs(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 1], [1, 1], [2, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 1],
                "arcs": [[[0, 0], [1, 0], [2, 0]], [[0, 1], [1, 1], [2, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0]},
                    "bar": {"type": "LineString", "arcs": [1]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_abc_extends_an_old_arc_ab_they_share_the_arc_ab(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 0],
                "arcs": [[[0, 0], [1, 0]], [[1, 0], [2, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0]},
                    "bar": {"type": "LineString", "arcs": [0, 1]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_abc_extends_a_reversed_old_arc_ba_they_share_the_arc_ba(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[1, 0], [0, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 0],
                "arcs": [[[1, 0], [0, 0]], [[1, 0], [2, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0]},
                    "bar": {"type": "LineString", "arcs": [~0, 1]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_starts_bc_in_the_middle_of_an_old_arc_abc_they_share_the_arc_bc(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[1, 0], [2, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 0],
                "arcs": [[[0, 0], [1, 0]], [[1, 0], [2, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [1]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_bc_starts_in_the_middle_of_a_reversed_old_arc_cba_they_share_the_arc_cb(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[2, 0], [1, 0], [0, 0]]},
                "bar": {"type": "LineString", "coordinates": [[1, 0], [2, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 0],
                "arcs": [[[2, 0], [1, 0]], [[1, 0], [0, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [~0]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_abd_deviates_from_an_old_arc_abc_they_share_the_arc_ab(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [3, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 3, 0],
                "arcs": [[[0, 0], [1, 0]], [[1, 0], [2, 0]], [[1, 0], [3, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [0, 2]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_abd_deviates_from_a_reversed_old_arc_cba_they_share_the_arc_ba(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[2, 0], [1, 0], [0, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [3, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 3, 0],
                "arcs": [[[2, 0], [1, 0]], [[1, 0], [0, 0]], [[1, 0], [3, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [~1, 2]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_dbc_merges_into_an_old_arc_abc_they_share_the_arc_bc(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[3, 0], [1, 0], [2, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 3, 0],
                "arcs": [[[0, 0], [1, 0]], [[1, 0], [2, 0]], [[3, 0], [1, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [2, 1]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_dbc_merges_into_a_reversed_old_arc_cba_they_share_the_arc_cb(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[2, 0], [1, 0], [0, 0]]},
                "bar": {"type": "LineString", "coordinates": [[3, 0], [1, 0], [2, 0]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 3, 0],
                "arcs": [[[2, 0], [1, 0]], [[1, 0], [0, 0]], [[3, 0], [1, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [2, ~0]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_dbe_shares_a_single_midpoint_with_an_old_arc_abc_they_share_the_point_b_but_no_arcs(
        self,
    ):
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "coordinates": [[0, 1], [1, 0], [2, 1]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 1],
                "arcs": [
                    [[0, 0], [1, 0]],
                    [[1, 0], [2, 0]],
                    [[0, 1], [1, 0]],
                    [[1, 0], [2, 1]],
                ],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1]},
                    "bar": {"type": "LineString", "arcs": [2, 3]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_abde_skips_a_point_with_an_old_arc_abcde_they_share_arcs_ab_and_de(
        self,
    ):
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],
                },
                "bar": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [3, 0], [4, 0]],
                },
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 4, 0],
                "arcs": [
                    [[0, 0], [1, 0]],
                    [[1, 0], [2, 0], [3, 0]],
                    [[3, 0], [4, 0]],
                    [[1, 0], [3, 0]],
                ],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1, 2]},
                    "bar": {"type": "LineString", "arcs": [0, 3, 2]},
                },
            },
            topology,
        )

    def test_topology_when_a_new_arc_abde_skips_a_point_with_a_reversed_old_arc_edcba_they_share_arcs_ba_and_ed(
        self,
    ):
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [[4, 0], [3, 0], [2, 0], [1, 0], [0, 0]],
                },
                "bar": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [3, 0], [4, 0]],
                },
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 4, 0],
                "arcs": [
                    [[4, 0], [3, 0]],
                    [[3, 0], [2, 0], [1, 0]],
                    [[1, 0], [0, 0]],
                    [[1, 0], [3, 0]],
                ],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1, 2]},
                    "bar": {"type": "LineString", "arcs": [~2, 3, ~0]},
                },
            },
            topology,
        )

    def test_topology_when_an_arc_abcdbe_self_intersects_it_is_still_one_arc(self):
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]],
                }
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 4, 0],
                "arcs": [[[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]]],
                "objects": {"foo": {"type": "LineString", "arcs": [0]}},
            },
            topology,
        )

    def test_topology_when_an_old_arc_abcdbe_self_intersects_and_shares_a_point_b_the_old_arc_has_multiple_cuts(
        self,
    ):
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]],
                },
                "bar": {"type": "LineString", "coordinates": [[0, 1], [1, 0], [2, 1]]},
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 4, 1],
                "arcs": [
                    [[0, 0], [1, 0]],
                    [[1, 0], [2, 0], [3, 0], [1, 0]],
                    [[1, 0], [4, 0]],
                    [[0, 1], [1, 0]],
                    [[1, 0], [2, 1]],
                ],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0, 1, 2]},
                    "bar": {"type": "LineString", "arcs": [3, 4]},
                },
            },
            topology,
        )

    def test_topology_when_an_arc_abca_is_closed_it_has_one_arc(self):
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [0, 1], [0, 0]],
                }
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 1, 1],
                "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                "objects": {"foo": {"type": "LineString", "arcs": [0]}},
            },
            topology,
        )

    def test_topology_exact_duplicate_closed_lines_abca_and_abca_share_the_arc_abca(
        self,
    ):
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [0, 1], [0, 0]],
                },
                "bar": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [0, 1], [0, 0]],
                },
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 1, 1],
                "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0]},
                    "bar": {"type": "LineString", "arcs": [0]},
                },
            },
            topology,
        )

    def test_topology_reversed_duplicate_closed_lines_abca_and_acba_share_the_arc_abca(
        self,
    ):
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [0, 1], [0, 0]],
                },
                "bar": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [0, 1], [1, 0], [0, 0]],
                },
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 1, 1],
                "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                "objects": {
                    "foo": {"type": "LineString", "arcs": [0]},
                    "bar": {"type": "LineString", "arcs": [~0]},
                },
            },
            topology,
        )

    def test_topology_coincident_closed_polygons_abca_and_bcab_share_the_arc_bcab(self):
        topology = self.topology(
            {
                "abca": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                },
                "bcab": {
                    "type": "Polygon",
                    "coordinates": [[[1, 0], [0, 1], [0, 0], [1, 0]]],
                },
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 1, 1],
                "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                "objects": {
                    "abca": {"type": "Polygon", "arcs": [[0]]},
                    "bcab": {"type": "Polygon", "arcs": [[0]]},
                },
            },
            topology,
        )

    def test_topology_coincident_reversed_closed_polygons_abca_and_bacb_share_the_arc_bcab(
        self,
    ):
        topology = self.topology(
            {
                "abca": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                },
                "bacb": {
                    "type": "Polygon",
                    "coordinates": [[[1, 0], [0, 0], [0, 1], [1, 0]]],
                },
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 1, 1],
                "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                "objects": {
                    "abca": {"type": "Polygon", "arcs": [[0]]},
                    "bacb": {"type": "Polygon", "arcs": [[~0]]},
                },
            },
            topology,
        )

    def test_topology_coincident_closed_polygons_abca_and_dbed_share_the_point_b(self):
        topology = self.topology(
            {
                "abca": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                },
                "dbed": {
                    "type": "Polygon",
                    "coordinates": [[[2, 1], [1, 0], [2, 2], [2, 1]]],
                },
            }
        )

        self.assertDictEqual(
            {
                "type": "Topology",
                "bbox": [0, 0, 2, 2],
                "arcs": [
                    [[1, 0], [0, 1], [0, 0], [1, 0]],
                    [[1, 0], [2, 2], [2, 1], [1, 0]],
                ],
                "objects": {
                    "abca": {"type": "Polygon", "arcs": [[0]]},
                    "dbed": {"type": "Polygon", "arcs": [[1]]},
                },
            },
            topology,
        )

    def test_topology_input_objects_are_mapped_to_topology_objects(self):
        """
        The topology `objects` is a map of geometry objects by name, allowing
        multiple GeoJSON geometry objects to share the same topology. When you
        pass multiple input files to bin/pytopojson, the basename of the file is
        used as the key, but you're welcome to edit the file to change it.
        """
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0.1, 0.2], [0.3, 0.4]]},
                "bar": {"type": "Polygon", "coordinates": [[[0.5, 0.6], [0.7, 0.8]]]},
            }
        )

        self.assertEqual(topology["objects"]["foo"]["type"], "LineString")
        self.assertEqual(topology["objects"]["bar"]["type"], "Polygon")

    def test_topology_features_are_mapped_to_geometries(self):
        """
        TopoJSON doesn't use features because you can represent the same
        information more compactly just by using geometry objects.
        """
        topology = self.topology(
            {
                "foo": {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                    },
                },
                "bar": {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0.5, 0.6], [0.7, 0.8]]],
                    },
                },
            }
        )

        self.assertEqual(topology["objects"]["foo"]["type"], "LineString")
        self.assertEqual(topology["objects"]["bar"]["type"], "Polygon")

    def test_topology_feature_collections_are_mapped_to_geometry_collections(self):
        topology = self.topology(
            {
                "collection": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",
                                "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                            },
                        },
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [[[0.5, 0.6], [0.7, 0.8]]],
                            },
                        },
                    ],
                }
            }
        )

        self.assertEqual(
            topology["objects"]["collection"]["type"], "GeometryCollection"
        )
        self.assertEqual(len(topology["objects"]["collection"]["geometries"]), 2)
        self.assertEqual(
            topology["objects"]["collection"]["geometries"][0]["type"], "LineString"
        )
        self.assertEqual(
            topology["objects"]["collection"]["geometries"][1]["type"], "Polygon"
        )

    def test_topology_nested_geometry_collections(self):
        topology = self.topology(
            {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {
                            "type": "GeometryCollection",
                            "geometries": [
                                {
                                    "type": "LineString",
                                    "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                                }
                            ],
                        },
                        {"type": "Polygon", "coordinates": [[[0.5, 0.6], [0.7, 0.8]]]},
                    ],
                }
            }
        )

        self.assertEqual(
            len(
                topology["objects"]["collection"]["geometries"][0]["geometries"][0][
                    "arcs"
                ]
            ),
            1,
        )

    def test_topology_null_geometry_objects_are_preserved_in_geometry_collections(self):
        topology = self.topology(
            {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        None,
                        {"type": "Polygon", "coordinates": [[[0.5, 0.6], [0.7, 0.8]]]},
                    ],
                }
            }
        )

        self.assertEqual(
            topology["objects"]["collection"]["type"], "GeometryCollection"
        )
        self.assertEqual(len(topology["objects"]["collection"]["geometries"]), 2)
        self.assertEqual(
            topology["objects"]["collection"]["geometries"][0]["type"], None
        )
        self.assertEqual(
            topology["objects"]["collection"]["geometries"][1]["type"], "Polygon"
        )

    def test_topology_features_with_null_geometry_objects_are_preserved_in_feature_collections(
        self,
    ):
        topology = self.topology(
            {
                "collection": {
                    "type": "FeatureCollection",
                    "features": [
                        {"type": "Feature", "geometry": None},
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [[[0.5, 0.6], [0.7, 0.8]]],
                            },
                        },
                    ],
                }
            }
        )

        self.assertEqual(
            topology["objects"]["collection"]["type"], "GeometryCollection"
        )
        self.assertEqual(len(topology["objects"]["collection"]["geometries"]), 2)
        self.assertEqual(
            topology["objects"]["collection"]["geometries"][0]["type"], None
        )
        self.assertEqual(
            topology["objects"]["collection"]["geometries"][1]["type"], "Polygon"
        )

    def test_topology_top_level_features_with_null_geometry_objects_are_preserved(self):
        topology = self.topology({"feature": {"type": "Feature", "geometry": None}})
        self.assertDictEqual({"feature": {"type": None}}, topology["objects"])

    def test_topology_converting_a_feature_to_a_geometry_preserves_its_id(self):
        """
        To know what a geometry object represents, specify an id. I prefer
        numeric identifiers, such as ISO 3166-1 numeric, but strings work too.
        """
        topology = self.topology(
            {
                "foo": {
                    "type": "Feature",
                    "id": 42,
                    "properties": {},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                    },
                }
            }
        )

        self.assertEqual(topology["objects"]["foo"]["type"], "LineString")
        self.assertEqual(topology["objects"]["foo"]["id"], 42)

    def test_topology_converting_a_feature_to_a_geometry_preserves_its_bbox(self):
        topology = self.topology(
            {
                "foo": {
                    "type": "Feature",
                    "bbox": [0, 0, 10, 10],
                    "properties": {},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                    },
                }
            }
        )
        self.assertListEqual(topology["objects"]["foo"]["bbox"], [0, 0, 10, 10])

        topology = self.topology(
            {
                "foo": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "LineString",
                        "bbox": [0, 0, 10, 10],
                        "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                    },
                }
            }
        )
        self.assertListEqual(topology["objects"]["foo"]["bbox"], [0, 0, 10, 10])

    def test_topology_converting_a_feature_to_a_geometry_preserves_its_properties_but_only_if_non_empty(
        self,
    ):
        topology = self.topology(
            {
                "foo": {
                    "type": "Feature",
                    "id": "Foo",
                    "properties": {"name": "George"},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                    },
                }
            }
        )
        self.assertDictEqual(
            topology["objects"]["foo"]["properties"], {"name": "George"}
        )

        topology = self.topology(
            {
                "foo": {
                    "type": "Feature",
                    "id": "Foo",
                    "properties": {"name": "George"},
                    "geometry": {
                        "type": "GeometryCollection",
                        "geometries": [
                            {
                                "type": "LineString",
                                "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                            }
                        ],
                    },
                }
            }
        )
        self.assertDictEqual(
            topology["objects"]["foo"]["properties"], {"name": "George"}
        )

        topology = self.topology(
            {
                "foo": {
                    "type": "Feature",
                    "id": "Foo",
                    "properties": {"name": "George", "demeanor": "curious"},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                    },
                }
            }
        )
        self.assertDictEqual(
            {"name": "George", "demeanor": "curious"},
            topology["objects"]["foo"]["properties"],
        )

        topology = self.topology(
            {
                "foo": {
                    "type": "Feature",
                    "id": "Foo",
                    "properties": {},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[0.1, 0.2], [0.3, 0.4]],
                    },
                }
            }
        )
        self.assertEqual(None, topology["objects"]["foo"].get("properties", None))

    def test_topology_the_returned_transform_exactly_encompasses_the_input_geometry(
        self,
    ):
        """
        It's not required by the specification that the transform exactly
        encompass the input geometry, but this is a good test that the reference
        implementation is working correctly.
        """
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [[1 / 8, 1 / 16], [1 / 2, 1 / 4]],
                }
            },
            quantization=2,
        )
        self.assertDictEqual(
            {"scale": [3 / 8, 3 / 16], "translate": [1 / 8, 1 / 16]},
            topology["transform"],
        )

        topology = self.topology(
            {
                "foo": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [1 / 8, 1 / 16],
                            [1 / 2, 1 / 16],
                            [1 / 2, 1 / 4],
                            [1 / 8, 1 / 4],
                            [1 / 8, 1 / 16],
                        ]
                    ],
                }
            },
            quantization=2,
        )
        self.assertDictEqual(
            {"scale": [3 / 8, 3 / 16], "translate": [1 / 8, 1 / 16]},
            topology["transform"],
        )

    def test_topology_arc_coordinates_are_integers_with_delta_encoding(self):
        """
        TopoJSON uses integers with delta encoding to represent geometry
        efficiently. (Quantization is necessary for simplification anyway, so
        that we can identify which points are shared by contiguous geometry
        objects.) The delta encoding works particularly well because line strings
        are not random: most points are very close to their neighbors!
        """
        topology = self.topology(
            {
                "foo": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [1 / 8, 1 / 16],
                            [1 / 2, 1 / 16],
                            [1 / 2, 1 / 4],
                            [1 / 8, 1 / 4],
                            [1 / 8, 1 / 16],
                        ]
                    ],
                }
            },
            quantization=2,
        )
        self.assertListEqual(
            [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]], topology["arcs"][0]
        )

    def test_topology_points_coordinates_are_integers_with_delta_encoding(self):
        """
        TopoJSON uses integers with for points, also. However, there’s no delta-
        encoding, even for MultiPoints. And, unlike other geometry objects,
        points are still defined with coordinates rather than arcs.
        """
        topology = self.topology(
            {
                "foo": {"type": "Point", "coordinates": [1 / 8, 1 / 16]},
                "bar": {"type": "Point", "coordinates": [1 / 2, 1 / 4]},
            },
            quantization=2,
        )
        self.assertListEqual([], topology["arcs"])
        self.assertDictEqual(
            {"type": "Point", "coordinates": [0, 0]}, topology["objects"]["foo"]
        )
        self.assertDictEqual(
            {"type": "Point", "coordinates": [1, 1]}, topology["objects"]["bar"]
        )

        topology = self.topology(
            {
                "foo": {
                    "type": "MultiPoint",
                    "coordinates": [[1 / 8, 1 / 16], [1 / 2, 1 / 4]],
                }
            },
            quantization=2,
        )
        self.assertListEqual([], topology["arcs"])
        self.assertDictEqual(
            {"type": "MultiPoint", "coordinates": [[0, 0], [1, 1]]},
            topology["objects"]["foo"],
        )

    # def test_topology_quantization_rounds_to_the_closest_integer_coordinate_to_minimize_error(self):
    #     """
    #     Rounding is more accurate than flooring.
    #     """
    #     topology = self.topology({
    #         'foo': {
    #             'type': 'LineString',
    #             'coordinates': [
    #                 [['0'], ['0']],
    #                 [['5'], ['5']],
    #                 [['6'], ['6']],
    #                 [['0'], ['0']],
    #                 [['1'], ['1']],
    #                 [['9'], ['9']],
    #                 [['9'], ['9']],
    #                 [['5'], ['5']],
    #                 [['0'], ['0']],
    #                 [['4'], ['4']],
    #                 [['5'], ['5']],
    #                 [10, 10]
    #             ]
    #         }
    #     }, 11)
    #     self.assertListEqual([
    #         [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10]
    #     ], client['feature'](topology, topology['objects']['foo']['geometry']['coordinates']))
    #     self.assertListEqual([
    #         [[0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
    #     ], topology['arcs'])
    #     self.assertDictEqual({
    #         'scale': [1, 1],
    #         'translate': [0, 0]
    #     }, topology['transform'])

    # def test_topology_quantization_precisely_preserves_minimum_and_maximum_values(self):
    #     """
    #     When rounding, we must be careful not to exceed [±180°, ±90°]!
    #     """
    #     topology = self.topology({
    #         'foo': {
    #             'type': 'LineString',
    #             'coordinates': [[-180, -90], [0, 0], [180, 90]]
    #         }
    #     }, 3)
    #     self.assertListEqual([
    #         [-180, -90], [0, 0], [180, 90]
    #     ], client['feature'](topology, topology['objects']['foo']['geometry']['coordinates'])
    #     self.assertListEqual([
    #         [[0, 0], [1, 1], [1, 1]]
    #     ], topology['arcs'])
    #     self.assertDictEqual({
    #         'scale': [180, 90],
    #         'translate': [-180, -90]
    #     }, topology['transform'])

    def test_topology_precision_of_quantization_is_configurable(self):
        """
        GeoJSON inputs are in floating point format, so some error may creep in
        that prevents you from using exact match to determine shared points. The
        default quantization, 1e4, allows for 10,000 differentiable points in
        both dimensions. If you're using TopoJSON to represent especially high-
        precision geometry, you might want to increase the precision however,
        this necessarily increases the output size and the likelihood of seams
        between contiguous geometry after simplificatio[''] The quantization factor
        should be a power of ten for the most efficient representation, since
        JSON uses base-ten encoding for numbers.
        """
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [
                        [1 / 8, 1 / 16],
                        [1 / 2, 1 / 16],
                        [1 / 8, 1 / 4],
                        [1 / 2, 1 / 4],
                    ],
                }
            },
            3,
        )
        self.assertListEqual([[0, 0], [2, 0], [-2, 2], [2, 0]], topology["arcs"][0])
        topology = self.topology(
            {
                "foo": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [1 / 8, 1 / 16],
                            [1 / 2, 1 / 16],
                            [1 / 2, 1 / 4],
                            [1 / 8, 1 / 4],
                            [1 / 8, 1 / 16],
                        ]
                    ],
                }
            },
            5,
        )
        self.assertListEqual(
            [[0, 0], [4, 0], [0, 4], [-4, 0], [0, -4]], topology["arcs"][0]
        )

    def test_topology_coincident_points_are_removed(self):
        """
        Quantization may introduce coincident points, so these are remove['']
        """
        topology = self.topology(
            {
                "foo": {
                    "type": "LineString",
                    "coordinates": [
                        [1 / 8, 1 / 16],
                        [1 / 8, 1 / 16],
                        [1 / 2, 1 / 4],
                        [1 / 2, 1 / 4],
                    ],
                }
            },
            2,
        )
        self.assertListEqual([[[0, 0], [1, 1]]], topology["arcs"])
        topology = self.topology(
            {
                "foo": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [1 / 8, 1 / 16],
                            [1 / 2, 1 / 16],
                            [1 / 2, 1 / 16],
                            [1 / 2, 1 / 4],
                            [1 / 8, 1 / 4],
                            [1 / 8, 1 / 4],
                            [1 / 8, 1 / 16],
                        ]
                    ],
                }
            },
            2,
        )
        self.assertListEqual(
            [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]], topology["arcs"][0]
        )

    def test_topology_collapsed_lines_are_preserved(self):
        """
        Quantization may introduce degenerate features which have collapsed onto a single poin['']
        """
        topology = self.topology(
            {
                "foo": {"type": "LineString", "coordinates": [[0, 0], [1, 1], [2, 2]]},
                "bar": {
                    "type": "LineString",
                    "coordinates": [[-80, -80], [0, 0], [80, 80]],
                },
            },
            3,
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0]}, topology["objects"]["foo"]
        )
        self.assertListEqual([[1, 1], [0, 0]], topology["arcs"][0])

    def test_topology_collapsed_lines_in_a_multilinestring_are_preserved(self):
        topology = self.topology(
            {
                "foo": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [[1 / 8, 1 / 16], [1 / 2, 1 / 4]],
                        [[1 / 8, 1 / 16], [1 / 8, 1 / 16]],
                        [[1 / 2, 1 / 4], [1 / 8, 1 / 16]],
                    ],
                }
            },
            2,
        )
        self.assertEqual(len(topology["arcs"]), 2)
        self.assertListEqual([[0, 0], [0, 0]], topology["arcs"][1])
        self.assertListEqual([[0, 0], [1, 1]], topology["arcs"][0])
        self.assertListEqual([[0], [1], [~0]], topology["objects"]["foo"]["arcs"])

    def test_topology_collapsed_polygons_are_preserved(self):
        topology = self.topology(
            {
                "foo": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
                },
                "bar": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [0, 1], [1, 1], [0, 0]]],
                },
                "baz": {
                    "type": "MultiPoint",
                    "coordinates": [[-80, -80], [0, 0], [80, 80]],
                },
            },
            3,
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0]]}, topology["objects"]["foo"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0]]}, topology["objects"]["bar"]
        )
        self.assertListEqual([[1, 1], [0, 0]], topology["arcs"][0])

    def test_topology_collapsed_polygons_in_a_MultiPolygon_are_preserved(self):
        topology = self.topology(
            {
                "foo": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [1 / 8, 1 / 16],
                                [1 / 2, 1 / 16],
                                [1 / 2, 1 / 4],
                                [1 / 8, 1 / 4],
                                [1 / 8, 1 / 16],
                            ]
                        ],
                        [
                            [
                                [1 / 8, 1 / 16],
                                [1 / 8, 1 / 16],
                                [1 / 8, 1 / 16],
                                [1 / 8, 1 / 16],
                            ]
                        ],
                        [
                            [
                                [1 / 8, 1 / 16],
                                [1 / 8, 1 / 4],
                                [1 / 2, 1 / 4],
                                [1 / 2, 1 / 16],
                                [1 / 8, 1 / 16],
                            ]
                        ],
                    ],
                }
            },
            2,
        )
        self.assertTrue(0 < len(topology["arcs"]))
        self.assertTrue(2 <= len(topology["arcs"][0]))
        self.assertTrue(3 == len(topology["objects"]["foo"]["arcs"]))

    def test_topology_collapsed_geometries_in_a_GeometryCollection_are_preserved(self):
        topology = self.topology(
            {
                "collection": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {"type": "MultiPolygon", "coordinates": []},
                        }
                    ],
                }
            },
            2,
        )
        self.assertTrue(len(topology["arcs"]) == 0)
        self.assertDictEqual(
            {
                "type": "GeometryCollection",
                "geometries": [{"type": "MultiPolygon", "arcs": []}],
            },
            topology["objects"]["collection"],
        )

    def test_topology_empty_geometries_are_not_removed(self):
        """
        If one of the top-level objects in the input is empty, however, it is
        still preserved in the output
        """
        topology = self.topology(
            {"foo": {"type": "MultiPolygon", "coordinates": []}}, 2
        )
        self.assertTrue(0 == len(topology["arcs"]))
        self.assertDictEqual(
            {"type": "MultiPolygon", "arcs": []}, topology["objects"]["foo"]
        )

    def test_topology_empty_polygons_are_not_removed(self):
        topology = self.topology(
            {
                "foo": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {"type": "MultiPolygon", "coordinates": [[]]},
                        }
                    ],
                },
                "bar": {"type": "Polygon", "coordinates": []},
            }
        )
        self.assertTrue(0 == len(topology["arcs"]))
        self.assertDictEqual(
            {
                "type": "GeometryCollection",
                "geometries": [{"type": "MultiPolygon", "arcs": [[]]}],
            },
            topology["objects"]["foo"],
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": []}, topology["objects"]["bar"]
        )

    def test_topology_the_lines_ab_and_ab_share_the_same_arc(self):
        """

        A-----B

        """
        topology = self.topology(
            {
                "ab": {"type": "LineString", "coordinates": [[0, 0], [0, 1]]},
                "ba": {"type": "LineString", "coordinates": [[0, 0], [0, 1]]},
            }
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0]}, topology["objects"]["ab"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0]}, topology["objects"]["ba"]
        )

    def test_topology_the_lines_ab_and_ba_share_the_same_arc(self):
        """

        A-----B

        """
        topology = self.topology(
            {
                "ab": {"type": "LineString", "coordinates": [[0, 0], [0, 1]]},
                "ba": {"type": "LineString", "coordinates": [[0, 1], [0, 0]]},
            }
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0]}, topology["objects"]["ab"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [~0]}, topology["objects"]["ba"]
        )

    def test_topology_the_lines_acd_and_bcd_share_three_arcs(self):
        """

        A
         \
          \
           \
            \
             \
        B-----C-----D

        """
        topology = self.topology(
            {
                "acd": {"type": "LineString", "coordinates": [[0, 0], [1, 1], [2, 1]]},
                "bcd": {"type": "LineString", "coordinates": [[0, 1], [1, 1], [2, 1]]},
            }
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1]}, topology["objects"]["acd"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [2, 1]}, topology["objects"]["bcd"]
        )

    def test_topology_the_lines_acd_and_dcb_share_three_arcs(self):
        """

        A
         \
          \
           \
            \
             \
        B-----C-----D

        """
        topology = self.topology(
            {
                "acd": {"type": "LineString", "coordinates": [[0, 0], [1, 1], [2, 1]]},
                "dcb": {"type": "LineString", "coordinates": [[2, 1], [1, 1], [0, 1]]},
            },
            quantization=3,
        )
        self.assertListEqual(
            [[[0, 0], [1, 2]], [[1, 2], [1, 0]], [[1, 2], [-1, 0]]],  # AC  # CD  # CB
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1]}, topology["objects"]["acd"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [~1, 2]}, topology["objects"]["dcb"]
        )

    def test_topology_the_lines_acdf_and_bcdf_share_three_arcs(self):
        """

        A
         \
          \
           \
            \
             \
        B-----C-----D-----F
        """
        topology = self.topology(
            {
                "acdf": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 1]],
                },
                "bcdf": {
                    "type": "LineString",
                    "coordinates": [[0, 1], [1, 1], [2, 1], [3, 1]],
                },
            },
            4,
        )
        self.assertListEqual(
            [
                [[0, 0], [1, 3]],  # AC
                [[1, 3], [1, 0], [1, 0]],  # CDF
                [[0, 3], [1, 0]],  # BC
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1]}, topology["objects"]["acdf"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [2, 1]}, topology["objects"]["bcdf"]
        )

    def test_topology_the_lines_bcde_and_bcdf_share_three_arcs(self):
        """

                          E
                         /
                        /
                       /
                      /
                     /
        B-----C-----D-----F
        """
        topology = self.topology(
            {
                "bcde": {
                    "type": "LineString",
                    "coordinates": [[0, 1], [1, 1], [2, 1], [3, 0]],
                },
                "bcdf": {
                    "type": "LineString",
                    "coordinates": [[0, 1], [1, 1], [2, 1], [3, 1]],
                },
            },
            4,
        )
        self.assertListEqual(
            [
                [[0, 3], [1, 0], [1, 0]],  # BCD
                [[2, 3], [1, -3]],  # DE
                [[2, 3], [1, 0]],  # DF
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1]}, topology["objects"]["bcde"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 2]}, topology["objects"]["bcdf"]
        )

    def test_topology_the_lines_acde_and_cd_share_three_arcs(self):
        r"""

        A                 E
         \               /
          \             /
           \           /
            \         /
             \       /
              C-----D

        """
        topology = self.topology(
            {
                "acde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 0]],
                },
                "cd": {"type": "LineString", "coordinates": [[1, 1], [2, 1]]},
            },
            4,
        )
        self.assertListEqual(
            [[[0, 0], [1, 3]], [[1, 3], [1, 0]], [[2, 3], [1, -3]]],  # AC  # CD  # DE
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1, 2]}, topology["objects"]["acde"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [1]}, topology["objects"]["cd"]
        )

    def test_topology_the_lines_acde_and_bcd_share_four_arcs(self):
        r"""

        A                 E
         \               /
          \             /
           \           /
            \         /
             \       /
        B-----C-----D

        """
        topology = self.topology(
            {
                "acde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 0]],
                },
                "bcd": {"type": "LineString", "coordinates": [[0, 1], [1, 1], [2, 1]]},
            },
            4,
        )
        self.assertListEqual(
            [
                [[0, 0], [1, 3]],  # AC
                [[1, 3], [1, 0]],  # CD
                [[2, 3], [1, -3]],  # DE
                [[0, 3], [1, 0]],  # BC
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1, 2]}, topology["objects"]["acde"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [3, 1]}, topology["objects"]["bcd"]
        )

    def test_topology_the_lines_acde_and_cdf_share_four_arcs(self):
        r"""

        A                 E
         \               /
          \             /
           \           /
            \         /
             \       /
              C-----D-----F

        """
        topology = self.topology(
            {
                "acde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 0]],
                },
                "cdf": {"type": "LineString", "coordinates": [[1, 1], [2, 1], [3, 1]]},
            },
            4,
        )
        self.assertListEqual(
            [
                [[0, 0], [1, 3]],  # AC
                [[1, 3], [1, 0]],  # CD
                [[2, 3], [1, -3]],  # DE
                [[2, 3], [1, 0]],  # CF
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1, 2]}, topology["objects"]["acde"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [1, 3]}, topology["objects"]["cdf"]
        )

    def test_topology_the_lines_acde_and_bcdf_share_five_arcs(self):
        r"""

        A                 E
         \               /
          \             /
           \           /
            \         /
             \       /
        B-----C-----D-----F

        """
        topology = self.topology(
            {
                "acde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 0]],
                },
                "bcdf": {
                    "type": "LineString",
                    "coordinates": [[0, 1], [1, 1], [2, 1], [3, 1]],
                },
            },
            4,
        )
        self.assertListEqual(
            [
                [[0, 0], [1, 3]],  # AC
                [[1, 3], [1, 0]],  # CD
                [[2, 3], [1, -3]],  # DE
                [[0, 3], [1, 0]],  # BC
                [[2, 3], [1, 0]],  # DF
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1, 2]}, topology["objects"]["acde"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [3, 1, 4]}, topology["objects"]["bcdf"]
        )

    def test_topology_the_lines_acde_edca_and_acdf_share_three_arcs(self):
        r"""

        A                 E
         \               /
          \             /
           \           /
            \         /
             \       /
              C-----D-----F

        """
        topology = self.topology(
            {
                "acde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 0]],
                },
                "edca": {
                    "type": "LineString",
                    "coordinates": [[3, 0], [2, 1], [1, 1], [0, 0]],
                },
                "acdf": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 1]],
                },
            },
            4,
        )
        self.assertListEqual(
            [
                [[0, 0], [1, 3], [1, 0]],  # ACD
                [[2, 3], [1, -3]],  # DE
                [[2, 3], [1, 0]],  # DF
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1]}, topology["objects"]["acde"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 2]}, topology["objects"]["acdf"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [~1, ~0]}, topology["objects"]["edca"]
        )

    def test_topology_the_lines_acde_acdf_and_edca_share_three_arcs(self):
        r"""

        A                 E
         \               /
          \             /
           \           /
            \         /
             \       /
              C-----D-----F

        """
        topology = self.topology(
            {
                "acde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 0]],
                },
                "acdf": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 1]],
                },
                "edca": {
                    "type": "LineString",
                    "coordinates": [[3, 0], [2, 1], [1, 1], [0, 0]],
                },
            },
            4,
        )
        self.assertListEqual(
            [
                [[0, 0], [1, 3], [1, 0]],  # ACD
                [[2, 3], [1, -3]],  # DE
                [[2, 3], [1, 0]],  # DF
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1]}, topology["objects"]["acde"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 2]}, topology["objects"]["acdf"]
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [~1, ~0]}, topology["objects"]["edca"]
        )

    def test_topology_the_lines_acde_acdf_bcde_and_bcdf_and_their_reversals_share_five_arcs(
        self,
    ):
        r"""

        A                 E
         \               /
          \             /
           \           /
            \         /
             \       /
        B-----C-----D-----F

        """
        topology = self.topology(
            {
                "acde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 0]],
                },
                "acdf": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 1], [2, 1], [3, 1]],
                },
                "bcde": {
                    "type": "LineString",
                    "coordinates": [[0, 1], [1, 1], [2, 1], [3, 0]],
                },
                "bcdf": {
                    "type": "LineString",
                    "coordinates": [[0, 1], [1, 1], [2, 1], [3, 1]],
                },
                "edca": {
                    "type": "LineString",
                    "coordinates": [[3, 0], [2, 1], [1, 1], [0, 0]],
                },
                "fdca": {
                    "type": "LineString",
                    "coordinates": [[3, 1], [2, 1], [1, 1], [0, 0]],
                },
                "edcb": {
                    "type": "LineString",
                    "coordinates": [[3, 0], [2, 1], [1, 1], [0, 1]],
                },
                "fdcb": {
                    "type": "LineString",
                    "coordinates": [[3, 1], [2, 1], [1, 1], [0, 1]],
                },
            },
            4,
        )
        self.assertListEqual(
            topology["arcs"],
            [
                [[0, 0], [1, 3]],  # AC
                [[1, 3], [1, 0]],  # CD
                [[2, 3], [1, -3]],  # DE
                [[2, 3], [1, 0]],  # DF
                [[0, 3], [1, 0]],  # BC
            ],
        )
        self.assertDictEqual(
            topology["objects"]["acde"], {"type": "LineString", "arcs": [0, 1, 2]}
        )
        self.assertDictEqual(
            topology["objects"]["acdf"], {"type": "LineString", "arcs": [0, 1, 3]}
        )
        self.assertDictEqual(
            topology["objects"]["bcde"], {"type": "LineString", "arcs": [4, 1, 2]}
        )
        self.assertDictEqual(
            topology["objects"]["bcdf"], {"type": "LineString", "arcs": [4, 1, 3]}
        )
        self.assertDictEqual(
            topology["objects"]["edca"], {"type": "LineString", "arcs": [~2, ~1, ~0]}
        )
        self.assertDictEqual(
            topology["objects"]["fdca"], {"type": "LineString", "arcs": [~3, ~1, ~0]}
        )
        self.assertDictEqual(
            topology["objects"]["edcb"], {"type": "LineString", "arcs": [~2, ~1, ~4]}
        )
        self.assertDictEqual(
            topology["objects"]["fdcb"], {"type": "LineString", "arcs": [~3, ~1, ~4]}
        )

    def test_topology_the_polygons_abcda_and_befcb_share_three_arcs(self):
        """

        A-----B-----E
        |     |     |
        |     |     |
        |     |     |
        |     |     |
        |     |     |
        D-----C-----F

        """
        topology = self.topology(
            {
                "abcda": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                },
                "befcb": {
                    "type": "Polygon",
                    "coordinates": [[[1, 0], [2, 0], [2, 1], [1, 1], [1, 0]]],
                },
            },
            3,
        )
        self.assertListEqual(
            topology["arcs"],
            [
                [[1, 0], [0, 2]],  # BC
                [[1, 2], [-1, 0], [0, -2], [1, 0]],  # CDAB
                [[1, 0], [1, 0], [0, 2], [-1, 0]],  # BEFC
            ],
        )
        self.assertDictEqual(
            topology["objects"]["abcda"], {"type": "Polygon", "arcs": [[0, 1]]}
        )
        self.assertDictEqual(
            topology["objects"]["befcb"], {"type": "Polygon", "arcs": [[2, ~0]]}
        )

    def test_topology_the_polygons_abcda_and_abca_share_three_arcs(self):
        r"""

        A-----B
        |\    |
        | \   |
        |  \  |
        |   \ |
        |    \|
        D-----C

        """
        topology = self.topology(
            {
                "abcda": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                },
                "abca": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                },
            },
            2,
        )
        self.assertListEqual(
            [
                [[0, 0], [1, 0], [0, 1]],  # ABC
                [[1, 1], [-1, 0], [0, -1]],  # CDA
                [[1, 1], [-1, -1]],  # CA
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            topology["objects"]["abcda"], {"type": "Polygon", "arcs": [[0, 1]]}
        )
        self.assertDictEqual(
            topology["objects"]["abca"], {"type": "Polygon", "arcs": [[0, 2]]}
        )

    def test_topology_the_lines_abcde_and_abde_share_two_arcs(self):
        """

                    C
                   / \
                  /   \
                 /     \
                /       \
               /         \
        A-----B-----------D-----E

        """
        topology = self.topology(
            {
                "abcde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],
                },
                "abde": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [3, 0], [4, 0]],
                },
            },
            5,
        )
        self.assertListEqual(
            topology["arcs"],
            [
                [[0, 0], [1, 0]],  # AB
                [[1, 0], [1, 0], [1, 0]],  # BCD
                [[3, 0], [1, 0]],  # DE
                [[1, 0], [2, 0]],  # BD
            ],
        )
        self.assertDictEqual(
            topology["objects"]["abcde"], {"type": "LineString", "arcs": [0, 1, 2]}
        )
        self.assertDictEqual(
            topology["objects"]["abde"], {"type": "LineString", "arcs": [0, 3, 2]}
        )

    def test_topology_the_polygons_abca_acda_and_bfcb_share_five_arcs(self):
        r"""

        A-----B
        |\    |\
        | \   | \
        |  \  |  \
        |   \ |   \
        |    \|    \
        D-----C-----F

        """
        topology = self.topology(
            {
                "abca": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                },
                "acda": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 1], [0, 1], [0, 0]]],
                },
                "bfcb": {
                    "type": "Polygon",
                    "coordinates": [[[1, 0], [2, 1], [1, 1], [1, 0]]],
                },
            },
            quantization=3,
        )

        self.assertListEqual(
            [
                [[0, 0], [1, 0]],  # AB
                [[1, 0], [0, 2]],  # BC
                [[1, 2], [-1, -2]],  # CA
                [[1, 2], [-1, 0], [0, -2]],  # CDA
                [[1, 0], [1, 2], [-1, 0]],  # BFC
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0, 1, 2]]}, topology["objects"]["abca"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[~2, 3]]}, topology["objects"]["acda"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[4, ~1]]}, topology["objects"]["bfcb"]
        )

    def test_topology_the_polygons_abca_befcb_and_egfe_share_six_arcs(self):
        r"""

        A-----B-----E
         \    |     |\
          \   |     | \
           \  |     |  \
            \ |     |   \
             \|     |    \
              C-----F-----G

        """
        topology = self.topology(
            {
                "abca": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                },
                "befcb": {
                    "type": "Polygon",
                    "coordinates": [[[1, 0], [2, 0], [2, 1], [1, 1], [1, 0]]],
                },
                "egfe": {
                    "type": "Polygon",
                    "coordinates": [[[2, 0], [3, 1], [2, 1], [2, 0]]],
                },
            },
            quantization=4,
        )

        self.assertListEqual(
            [
                [[1, 0], [0, 3]],  # BC
                [[1, 3], [-1, -3], [1, 0]],  # CAB
                [[1, 0], [1, 0]],  # BE
                [[2, 0], [0, 3]],  # EF
                [[2, 3], [-1, 0]],  # FC
                [[2, 0], [1, 3], [-1, 0]],  # EGF
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0, 1]]}, topology["objects"]["abca"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[2, 3, 4, ~0]]}, topology["objects"]["befcb"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[5, ~3]]}, topology["objects"]["egfe"]
        )

    def test_topology_the_polygons_abcda_abefgda_and_befgdcb_share_three_arcs(self):
        """
        //
        // A-----B-----E
        // |     |     |
        // |     |     |
        // D-----C     |
        // |           |
        // |           |
        // G-----------F
        //
        """
        topology = self.topology(
            {
                "abcda": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                },
                "abefgda": {
                    "type": "Polygon",
                    "coordinates": [
                        [[0, 0], [1, 0], [2, 0], [2, 2], [0, 2], [0, 1], [0, 0]]
                    ],
                },
                "befgdcb": {
                    "type": "Polygon",
                    "coordinates": [
                        [[1, 0], [2, 0], [2, 2], [0, 2], [0, 1], [1, 1], [1, 0]]
                    ],
                },
            },
            quantization=3,
        )

        self.assertListEqual(
            [
                [[1, 0], [0, 1], [-1, 0]],  # BCD
                [[0, 1], [0, -1], [1, 0]],  # DAB
                [[1, 0], [1, 0], [0, 2], [-2, 0], [0, -1]],  # BEFGD
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0, 1]]}, topology["objects"]["abcda"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[2, 1]]}, topology["objects"]["abefgda"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[2, ~0]]}, topology["objects"]["befgdcb"]
        )

    def test_topology_the_polygons_abcda_and_bcdab_share_one_arc(self):
        """
        //
        // A-----B
        // |     |
        // |     |
        // D-----C
        //
        """
        topology = self.topology(
            {
                "abcda": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                },
                "bcdab": {
                    "type": "Polygon",
                    "coordinates": [[[1, 0], [1, 1], [0, 1], [0, 0], [1, 0]]],
                },
            },
            quantization=2,
        )

        self.assertListEqual(
            [[[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]]], topology["arcs"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0]]}, topology["objects"]["abcda"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0]]}, topology["objects"]["bcdab"]
        )

    def test_topology_the_polygons_abcda_ehgfe_and_efghe_share_two_arcs(self):
        """
        //
        // A-----------------B
        // |                 |
        // |                 |
        // |     E-----F     |
        // |     |     |     |
        // |     |     |     |
        // |     H-----G     |
        // |                 |
        // |                 |
        // D-----------------C
        //
        """
        topology = self.topology(
            {
                "abcda": {
                    "type": "Polygon",
                    "coordinates": [
                        [[0, 0], [3, 0], [3, 3], [0, 3], [0, 0]],
                        [[1, 1], [1, 2], [2, 2], [2, 1], [1, 1]],
                    ],
                },
                "efghe": {
                    "type": "Polygon",
                    "coordinates": [[[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]],
                },
            },
            quantization=4,
        )

        self.assertListEqual(
            [
                [[0, 0], [3, 0], [0, 3], [-3, 0], [0, -3]],  # ABCDA
                [[1, 1], [0, 1], [1, 0], [0, -1], [-1, 0]],  # EHGFE
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0], [1]]}, topology["objects"]["abcda"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[~1]]}, topology["objects"]["efghe"]
        )

    def test_topology_the_polygons_abcda_ehgfe_and_fghef_share_two_arcs(self):
        """
        //
        // A-----------------B
        // |                 |
        // |                 |
        // |     E-----F     |
        // |     |     |     |
        // |     |     |     |
        // |     H-----G     |
        // |                 |
        // |                 |
        // D-----------------C
        //
        """
        topology = self.topology(
            {
                "abcda": {
                    "type": "Polygon",
                    "coordinates": [
                        [[0, 0], [3, 0], [3, 3], [0, 3], [0, 0]],
                        [[1, 1], [1, 2], [2, 2], [2, 1], [1, 1]],
                    ],
                },
                "fghef": {
                    "type": "Polygon",
                    "coordinates": [[[2, 1], [2, 2], [1, 2], [1, 1], [2, 1]]],
                },
            },
            quantization=4,
        )

        self.assertListEqual(
            [
                [[0, 0], [3, 0], [0, 3], [-3, 0], [0, -3]],  # ABCDA
                [[1, 1], [0, 1], [1, 0], [0, -1], [-1, 0]],  # EHGFE
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[0], [1]]}, topology["objects"]["abcda"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[~1]]}, topology["objects"]["fghef"]
        )

    def test_topology_the_polygon_bcdb_and_the_line_string_abe_share_three_arcs(self):
        r"""
           C-----D
            \   /
             \ /
        A-----B-----E
        """
        topology = self.topology(
            {
                "abe": {"type": "LineString", "coordinates": [[0, 1], [2, 1], [4, 1]]},
                "bcdb": {
                    "type": "Polygon",
                    "coordinates": [[[2, 1], [1, 0], [3, 0], [2, 1]]],
                },
            },
            quantization=5,
        )

        self.assertListEqual(
            [
                [[0, 4], [2, 0]],  # AB
                [[2, 4], [2, 0]],  # BE
                [[2, 4], [-1, -4], [2, 0], [-1, 4]],  # BCDB
            ],
            topology["arcs"],
        )
        self.assertDictEqual(
            {"type": "LineString", "arcs": [0, 1]}, topology["objects"]["abe"]
        )
        self.assertDictEqual(
            {"type": "Polygon", "arcs": [[2]]}, topology["objects"]["bcdb"]
        )
