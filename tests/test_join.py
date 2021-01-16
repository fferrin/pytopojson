import unittest

from pytopojson import (
    extract,
    join,
)


class JoinTestCase(unittest.TestCase):
    def setUp(self):
        self.extract = extract.Extract()
        self.join = join.Join()

    def test_join_the_returned_hashmap_has_true_for_junction_points(self):
        junctions = self.join(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "ab": {"type": "LineString", "arcs": [[0, 0], [1, 0]]},
                }
            )
        )

        self.assertEqual(junctions.has([2, 0]), True)
        self.assertEqual(junctions.has([0, 0]), True)

    def test_join_the_returned_hashmap_has_undefined_for_non_junction_points(self):
        junctions = self.join(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "ab": {"type": "LineString", "arcs": [[0, 0], [2, 0]]},
                }
            )
        )

        self.assertEqual(junctions.has([1, 0]), False)

    def test_join_exact_duplicate_lines_abc_and_abc_have_junctions_at_their_end_points(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "abc2": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [2, 0]])

    def test_join_reversed_duplicate_lines_abc_and_cba_have_junctions_at_their_end_points(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [2, 0]])

    def test_join_exact_duplicate_rings_abca_and_abca_have_no_junctions(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]],
                    },
                    "abca2": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_reversed_duplicate_rings_acba_and_abca_have_no_junctions(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]],
                    },
                    "acba": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [2, 0], [1, 0], [0, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_rotated_duplicate_rings_bcab_and_abca_have_no_junctions(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]],
                    },
                    "bcab": {
                        "type": "Polygon",
                        "arcs": [[[1, 0], [2, 0], [0, 0], [1, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_ring_abca_and_line_abca_have_a_junction_at_a(self):
        junctions = self.join(
            self.extract(
                {
                    "abcaLine": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [2, 0], [0, 0]],
                    },
                    "abcaPolygon": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0]])

    def test_join_ring_bcab_and_line_abca_have_a_junction_at_a(self):
        junctions = self.join(
            self.extract(
                {
                    "abcaLine": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [2, 0], [0, 0]],
                    },
                    "bcabPolygon": {
                        "type": "Polygon",
                        "arcs": [[[1, 0], [2, 0], [0, 0], [1, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0]])

    def test_join_ring_abca_and_line_bcab_have_a_junction_at_b(self):
        junctions = self.join(
            self.extract(
                {
                    "bcabLine": {
                        "type": "LineString",
                        "arcs": [[1, 0], [2, 0], [0, 0], [1, 0]],
                    },
                    "abcaPolygon": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[1, 0]])

    def test_join_when_an_old_arc_abc_extends_a_new_arc_ab_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "ab": {"type": "LineString", "arcs": [[0, 0], [1, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [1, 0], [2, 0]])

    def test_join_when_a_reversed_old_arc_cba_extends_a_new_arc_ab_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "ab": {"type": "LineString", "arcs": [[0, 0], [1, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [1, 0], [2, 0]])

    def test_join_when_a_new_arc_ade_shares_its_start_with_an_old_arc_abc_there_is_a_junction_at_a(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "ade": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 1], [2, 1]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [2, 0], [2, 1]])

    def test_join_ring_aba_has_no_junctions(self):
        junctions = self.join(
            self.extract(
                {"aba": {"type": "Polygon", "arcs": [[[0, 0], [1, 0], [0, 0]]]}}
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_ring_aa_has_no_junctions(self):
        junctions = self.join(
            self.extract({"aa": {"type": "Polygon", "arcs": [[[0, 0], [0, 0]]]}})
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_degenerate_ring_a_has_no_junctions(self):
        junctions = self.join(
            self.extract({"a": {"type": "Polygon", "arcs": [[[0, 0]]]}})
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_when_a_new_line_dec_shares_its_end_with_an_old_line_abc_there_is_a_junction_at_c(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "dec": {"type": "LineString", "arcs": [[0, 1], [1, 1], [2, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [2, 0], [0, 1]])

    def test_join_when_a_new_line_abc_extends_an_old_line_ab_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "ab": {"type": "LineString", "arcs": [[0, 0], [1, 0]]},
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [1, 0], [2, 0]])

    def test_join_when_a_new_line_abc_extends_a_reversed_old_line_ba_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "ba": {"type": "LineString", "arcs": [[1, 0], [0, 0]]},
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [1, 0], [2, 0]])

    def test_join_when_a_new_line_starts_bc_in_the_middle_of_an_old_line_abc_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "bc": {"type": "LineString", "arcs": [[1, 0], [2, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [1, 0], [2, 0]])

    def test_join_when_a_new_line_bc_starts_in_the_middle_of_a_reversed_old_line_cba_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "bc": {"type": "LineString", "arcs": [[1, 0], [2, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [1, 0], [2, 0]])

    def test_join_when_a_new_line_abd_deviates_from_an_old_line_abc_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "abd": {"type": "LineString", "arcs": [[0, 0], [1, 0], [3, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [2, 0], [1, 0], [3, 0]])

    def test_join_when_a_new_line_abd_deviates_from_a_reversed_old_line_cba_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "abd": {"type": "LineString", "arcs": [[0, 0], [1, 0], [3, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[2, 0], [0, 0], [1, 0], [3, 0]])

    def test_join_when_a_new_line_dbc_merges_into_an_old_line_abc_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "dbc": {"type": "LineString", "arcs": [[3, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [2, 0], [1, 0], [3, 0]])

    def test_join_when_a_new_line_dbc_merges_into_a_reversed_old_line_cba_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "dbc": {"type": "LineString", "arcs": [[3, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[2, 0], [0, 0], [1, 0], [3, 0]])

    def test_join_when_a_new_line_dbe_shares_a_single_midpoint_with_an_old_line_abc_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "dbe": {"type": "LineString", "arcs": [[0, 1], [1, 0], [2, 1]]},
                }
            )
        )

        self.assertCountEqual(
            junctions.values(), [[0, 0], [2, 0], [2, 1], [1, 0], [0, 1]]
        )

    def test_join_when_a_new_line_abde_skips_a_point_with_an_old_line_abcde_there_is_a_junction_at_b_and_d(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abcde": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],
                    },
                    "abde": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [3, 0], [4, 0]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [4, 0], [1, 0], [3, 0]])

    def test_join_when_a_new_line_abde_skips_a_point_with_a_reversed_old_line_edcba_there_is_a_junction_at_b_and_d(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "edcba": {
                        "type": "LineString",
                        "arcs": [[4, 0], [3, 0], [2, 0], [1, 0], [0, 0]],
                    },
                    "abde": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [3, 0], [4, 0]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[4, 0], [0, 0], [1, 0], [3, 0]])

    def test_join_when_a_line_abcdbe_self_intersects_with_its_middle_there_are_no_junctions(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abcdbe": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]],
                    }
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [4, 0]])

    def test_join_when_a_line_abacd_self_intersects_with_its_start_there_are_no_junctions(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abacd": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [0, 0], [3, 0], [4, 0]],
                    }
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [4, 0]])

    def test_join_when_a_line_abcdbd_self_intersects_with_its_end_there_are_no_junctions(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abcdbd": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [4, 0], [3, 0], [4, 0]],
                    }
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0], [4, 0]])

    def test_join_when_an_old_line_abcdbe_self_intersects_and_shares_a_point_b_there_is_a_junction_at_b(
        self,
    ):
        junctions = self.join(
            self.extract(
                {
                    "abcdbe": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]],
                    },
                    "fbg": {"type": "LineString", "arcs": [[0, 1], [1, 0], [2, 1]]},
                }
            )
        )

        self.assertCountEqual(
            junctions.values(), [[0, 0], [4, 0], [1, 0], [0, 1], [2, 1]]
        )

    def test_join_when_a_line_abca_is_closed_there_is_a_junction_at_a(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [0, 1], [0, 0]],
                    }
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[0, 0]])

    def test_join_when_a_ring_abca_is_closed_there_are_no_junctions(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    }
                }
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_exact_duplicate_rings_abca_and_abca_share_the_arc_abca(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    },
                    "abca2": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_reversed_duplicate_rings_abca_and_acba_share_the_arc_abca(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    },
                    "acba": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [0, 1], [1, 0], [0, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_coincident_rings_abca_and_bcab_share_the_arc_bcab(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    },
                    "bcab": {
                        "type": "Polygon",
                        "arcs": [[[1, 0], [0, 1], [0, 0], [1, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_coincident_rings_abca_and_bacb_share_the_arc_bcab(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    },
                    "bacb": {
                        "type": "Polygon",
                        "arcs": [[[1, 0], [0, 0], [0, 1], [1, 0]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [])

    def test_join_coincident_rings_abca_and_dbed_share_the_point_b(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    },
                    "dbed": {
                        "type": "Polygon",
                        "arcs": [[[2, 1], [1, 0], [2, 2], [2, 1]]],
                    },
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[1, 0]])

    def test_join_coincident_ring_abca_and_line_dbe_share_the_point_b(self):
        junctions = self.join(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    },
                    "dbe": {"type": "LineString", "arcs": [[2, 1], [1, 0], [2, 2]]},
                }
            )
        )

        self.assertCountEqual(junctions.values(), [[2, 1], [2, 2], [1, 0]])
