import unittest

from pytopojson import (
    cut,
    extract,
)


class CutTestCase(unittest.TestCase):
    def setUp(self):
        self.cut = cut.Cut()
        self.extract = extract.Extract()

    def test_cut_exact_duplicate_lines_abc_and_abc_have_no_cuts(self):
        c = self.cut(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "abc2": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "abc": {"type": "LineString", "arcs": {0: 0, 1: 2}},
                "abc2": {"type": "LineString", "arcs": {0: 3, 1: 5}},
            },
            c["objects"],
        )

    def test_cut_reversed_duplicate_lines_abc_and_cba_have_no_cuts(self):
        c = self.cut(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "abc": {"type": "LineString", "arcs": {0: 0, 1: 2}},
                "cba": {"type": "LineString", "arcs": {0: 3, 1: 5}},
            },
            c["objects"],
        )

    def test_cut_exact_duplicate_rings_abca_and_abca_have_no_cuts(self):
        c = self.cut(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]],
                    },
                    "abca2": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [2, 0], [1, 0], [0, 0]]],
                    },
                }
            )
        )

        self.assertDictEqual(
            {
                "abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]},
                "abca2": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_reversed_duplicate_rings_acba_and_abca_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]},
                "acba": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_rotated_duplicate_rings_bcab_and_abca_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]},
                "bcab": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_ring_abca_and_line_abca_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abcaLine": {"type": "LineString", "arcs": {0: 0, 1: 3}},
                "abcaPolygon": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_ring_bcab_and_line_abca_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abcaLine": {"type": "LineString", "arcs": {0: 0, 1: 3}},
                "bcabPolygon": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_ring_abca_and_line_bcab_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "bcabLine": {"type": "LineString", "arcs": {0: 0, 1: 3}},
                "abcaPolygon": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_when_an_old_arc_abc_extends_a_new_arc_ab_abc_is_cut_into_ab_bc(self):
        c = self.cut(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "ab": {"type": "LineString", "arcs": [[0, 0], [1, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "abc": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "ab": {"type": "LineString", "arcs": {0: 3, 1: 4}},
            },
            c["objects"],
        )

    def test_cut_when_a_reversed_old_arc_cba_extends_a_new_arc_ab_cba_is_cut_into_cb_ba(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "ab": {"type": "LineString", "arcs": [[0, 0], [1, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "cba": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "ab": {"type": "LineString", "arcs": {0: 3, 1: 4}},
            },
            c["objects"],
        )

    def test_cut_when_a_new_arc_ade_shares_its_start_with_an_old_arc_abc_there_are_no_cuts(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "ade": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 1], [2, 1]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "ade": {"type": "LineString", "arcs": {0: 0, 1: 2}},
                "abc": {"type": "LineString", "arcs": {0: 3, 1: 5}},
            },
            c["objects"],
        )

    def test_cut_ring_aba_has_no_cuts(self):
        c = self.cut(
            self.extract(
                {"aba": {"type": "Polygon", "arcs": [[[0, 0], [1, 0], [0, 0]]]}}
            )
        )

        self.assertDictEqual(
            {"aba": {"type": "Polygon", "arcs": [{0: 0, 1: 2}]}}, c["objects"]
        )

    def test_cut_ring_aa_has_no_cuts(self):
        c = self.cut(
            self.extract({"aa": {"type": "Polygon", "arcs": [[[0, 0], [0, 0]]]}})
        )

        self.assertDictEqual(
            {"aa": {"type": "Polygon", "arcs": [{0: 0, 1: 1}]}}, c["objects"]
        )

    def test_cut_degenerate_ring_a_has_no_cuts(self):
        c = self.cut(self.extract({"a": {"type": "Polygon", "arcs": [[[0, 0]]]}}))

        self.assertDictEqual(
            {"a": {"type": "Polygon", "arcs": [{0: 0, 1: 0}]}}, c["objects"]
        )

    def test_cut_when_a_new_line_dec_shares_its_end_with_an_old_line_abc_there_are_no_cuts(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "dec": {"type": "LineString", "arcs": [[0, 1], [1, 1], [2, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "abc": {"type": "LineString", "arcs": {0: 0, 1: 2}},
                "dec": {"type": "LineString", "arcs": {0: 3, 1: 5}},
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_abc_extends_an_old_line_ab_abc_is_cut_into_ab_bc(self):
        c = self.cut(
            self.extract(
                {
                    "ab": {"type": "LineString", "arcs": [[0, 0], [1, 0]]},
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "ab": {"type": "LineString", "arcs": {0: 0, 1: 1}},
                "abc": {
                    "type": "LineString",
                    "arcs": {0: 2, 1: 3, "next": {0: 3, 1: 4}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_abc_extends_a_reversed_old_line_ba_abc_is_cut_into_ab_bc(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "ba": {"type": "LineString", "arcs": [[1, 0], [0, 0]]},
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "ba": {"type": "LineString", "arcs": {0: 0, 1: 1}},
                "abc": {
                    "type": "LineString",
                    "arcs": {0: 2, 1: 3, "next": {0: 3, 1: 4}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_starts_bc_in_the_middle_of_an_old_line_abc_abc_is_cut_into_ab_bc(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "bc": {"type": "LineString", "arcs": [[1, 0], [2, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "abc": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "bc": {"type": "LineString", "arcs": {0: 3, 1: 4}},
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_bc_starts_in_the_middle_of_a_reversed_old_line_cba_cba_is_cut_into_cb_ba(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "bc": {"type": "LineString", "arcs": [[1, 0], [2, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "cba": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "bc": {"type": "LineString", "arcs": {0: 3, 1: 4}},
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_abd_deviates_from_an_old_line_abc_abd_is_cut_into_ab_bd_and_abc_is_cut_into_ab_bc(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "abd": {"type": "LineString", "arcs": [[0, 0], [1, 0], [3, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "abc": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "abd": {
                    "type": "LineString",
                    "arcs": {0: 3, 1: 4, "next": {0: 4, 1: 5}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_abd_deviates_from_a_reversed_old_line_cba_cba_is_cut_into_cb_ba_and_abd_is_cut_into_ab_bd(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "abd": {"type": "LineString", "arcs": [[0, 0], [1, 0], [3, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "cba": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "abd": {
                    "type": "LineString",
                    "arcs": {0: 3, 1: 4, "next": {0: 4, 1: 5}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_dbc_merges_into_an_old_line_abc_dbc_is_cut_into_db_bc_and_abc_is_cut_into_ab_bc(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "dbc": {"type": "LineString", "arcs": [[3, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "abc": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "dbc": {
                    "type": "LineString",
                    "arcs": {0: 3, 1: 4, "next": {0: 4, 1: 5}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_dbc_merges_into_a_reversed_old_line_cba_dbc_is_cut_into_db_bc_and_cba_is_cut_into_cb_ba(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "cba": {"type": "LineString", "arcs": [[2, 0], [1, 0], [0, 0]]},
                    "dbc": {"type": "LineString", "arcs": [[3, 0], [1, 0], [2, 0]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "cba": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "dbc": {
                    "type": "LineString",
                    "arcs": {0: 3, 1: 4, "next": {0: 4, 1: 5}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_dbe_shares_a_single_midpoint_with_an_old_line_abc_dbe_is_cut_into_db_be_and_abc_is_cut_into_ab_bc(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "abc": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                    "dbe": {"type": "LineString", "arcs": [[0, 1], [1, 0], [2, 1]]},
                }
            )
        )

        self.assertDictEqual(
            {
                "abc": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 2}},
                },
                "dbe": {
                    "type": "LineString",
                    "arcs": {0: 3, 1: 4, "next": {0: 4, 1: 5}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_abde_skips_a_point_with_an_old_line_abcde_abde_is_cut_into_ab_bd_de_and_abcde_is_cut_into_ab_bcd_de(
        self,
    ):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abcde": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 3, "next": {0: 3, 1: 4}}},
                },
                "abde": {
                    "type": "LineString",
                    "arcs": {0: 5, 1: 6, "next": {0: 6, 1: 7, "next": {0: 7, 1: 8}}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_new_line_abde_skips_a_point_with_a_reversed_old_line_edcba_abde_is_cut_into_ab_bd_de_and_edcba_is_cut_into_ed_dcb_ba(
        self,
    ):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "edcba": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 3, "next": {0: 3, 1: 4}}},
                },
                "abde": {
                    "type": "LineString",
                    "arcs": {0: 5, 1: 6, "next": {0: 6, 1: 7, "next": {0: 7, 1: 8}}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_line_abcdbe_self_intersects_with_its_middle_it_is_not_cut(self):
        c = self.cut(
            self.extract(
                {
                    "abcdbe": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [2, 0], [3, 0], [1, 0], [4, 0]],
                    }
                }
            )
        )

        self.assertDictEqual(
            {"abcdbe": {"type": "LineString", "arcs": {0: 0, 1: 5}}}, c["objects"]
        )

    def test_cut_when_a_line_abacd_self_intersects_with_its_start_it_is_cut_into_aba_acd(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "abacd": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [0, 0], [3, 0], [4, 0]],
                    }
                }
            )
        )

        self.assertDictEqual(
            {
                "abacd": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 2, "next": {0: 2, 1: 4}},
                }
            },
            c["objects"],
        )

    def test_cut_when_a_line_abdcd_self_intersects_with_its_end_it_is_cut_into_abd_dcd(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "abdcd": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [0, 0], [3, 0], [4, 0]],
                    }
                }
            )
        )

        self.assertDictEqual(
            {
                "abdcd": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 2, "next": {0: 2, 1: 4}},
                }
            },
            c["objects"],
        )

    def test_cut_when_an_old_line_abcdbe_self_intersects_and_shares_a_point_b_abcdbe_is_cut_into_ab_bcdb_be_and_fbg_is_cut_into_fb_bg(
        self,
    ):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abcdbe": {
                    "type": "LineString",
                    "arcs": {0: 0, 1: 1, "next": {0: 1, 1: 4, "next": {0: 4, 1: 5}}},
                },
                "fbg": {
                    "type": "LineString",
                    "arcs": {0: 6, 1: 7, "next": {0: 7, 1: 8}},
                },
            },
            c["objects"],
        )

    def test_cut_when_a_line_abca_is_closed_there_are_no_cuts(self):
        c = self.cut(
            self.extract(
                {
                    "abca": {
                        "type": "LineString",
                        "arcs": [[0, 0], [1, 0], [0, 1], [0, 0]],
                    }
                }
            )
        )

        self.assertDictEqual(
            {"abca": {"type": "LineString", "arcs": {0: 0, 1: 3}}}, c["objects"]
        )

    def test_cut_when_a_ring_abca_is_closed_there_are_no_cuts(self):
        c = self.cut(
            self.extract(
                {
                    "abca": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [0, 1], [0, 0]]],
                    }
                }
            )
        )

        self.assertDictEqual(
            {"abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]}}, c["objects"]
        )

    def test_cut_exact_duplicate_rings_abca_and_abca_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]},
                "abca2": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_reversed_duplicate_rings_abca_and_acba_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]},
                "acba": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_coincident_rings_abca_and_bcab_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]},
                "bcab": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_coincident_rings_abca_and_bacb_have_no_cuts(self):
        c = self.cut(
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

        self.assertDictEqual(
            {
                "abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]},
                "bacb": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            c["objects"],
        )

    def test_cut_coincident_rings_abcda_efae_and_ghcg_are_cut_into_abc_cda_efae_and_ghcg(
        self,
    ):
        topology = self.cut(
            self.extract(
                {
                    "abcda": {
                        "type": "Polygon",
                        "arcs": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                    },
                    "efae": {
                        "type": "Polygon",
                        "arcs": [[[0, -1], [1, -1], [0, 0], [0, -1]]],
                    },
                    "ghcg": {
                        "type": "Polygon",
                        "arcs": [[[0, 2], [1, 2], [1, 1], [0, 2]]],
                    },
                }
            )
        )

        self.assertDictEqual(
            {
                "abcda": {
                    "type": "Polygon",
                    "arcs": [{0: 0, 1: 2, "next": {0: 2, 1: 4}}],
                },
                "efae": {"type": "Polygon", "arcs": [{0: 5, 1: 8}]},
                "ghcg": {"type": "Polygon", "arcs": [{0: 9, 1: 12}]},
            },
            topology["objects"],
        )

    def test_cut_coincident_rings_abca_and_dbed_have_no_cuts_but_are_rotated_to_share_b(
        self,
    ):
        topology = self.cut(
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

        self.assertDictEqual(
            {
                "abca": {"type": "Polygon", "arcs": [{0: 0, 1: 3}]},
                "dbed": {"type": "Polygon", "arcs": [{0: 4, 1: 7}]},
            },
            topology["objects"],
        )

        self.assertCountEqual(
            topology["coordinates"][0:4], [[1, 0], [0, 1], [0, 0], [1, 0]]
        )
        self.assertCountEqual(
            topology["coordinates"][4:8], [[1, 0], [2, 2], [2, 1], [1, 0]]
        )

    def test_cut_overlapping_rings_abcda_and_befcb_are_cut_into_bc_cdab_and_befc_cb(
        self,
    ):
        c = self.cut(
            self.extract(
                {
                    "abcda": {
                        "type": "Polygon",
                        "arcs": [
                            [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]
                        ],  # rotated to BCDAB, cut BC-CDAB
                    },
                    "befcb": {
                        "type": "Polygon",
                        "arcs": [[[1, 0], [2, 0], [2, 1], [1, 1], [1, 0]]],
                    },
                }
            )
        )

        self.assertDictEqual(
            {
                "abcda": {
                    "type": "Polygon",
                    "arcs": [{0: 0, 1: 1, "next": {0: 1, 1: 4}}],
                },
                "befcb": {
                    "type": "Polygon",
                    "arcs": [{0: 5, 1: 8, "next": {0: 8, 1: 9}}],
                },
            },
            c["objects"],
        )
