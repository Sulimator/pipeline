import unittest
import pandas as pd
from features.utils.selector import (
    extractor_factory,
    ExtractorNotFoundException,
)


class ExtractorSelectorTestCase(unittest.TestCase):
    def test_get_ztf_extractor(self):
        input_str = "ZTF"
        selected_extractor = extractor_factory(input_str)
        self.assertEqual(selected_extractor.NAME, "ztf_lc_features")

        input_str = "ztf"
        selected_extractor = extractor_factory(input_str)
        self.assertEqual(selected_extractor.NAME, "ztf_lc_features")

    def test_get_elasticc_extractor(self):
        input_str = "ELASTICC"
        selected_extractor = extractor_factory(input_str)
        self.assertEqual(
            selected_extractor([], [], []).NAME, "elasticc_lc_features"
        )

        input_str = "ELAsTiCC"
        selected_extractor = extractor_factory(input_str)
        self.assertEqual(
            selected_extractor([], [], []).NAME, "elasticc_lc_features"
        )

    def test_extractor_not_found(self):
        input_str = "dummy"
        with self.assertRaises(ExtractorNotFoundException):
            extractor_factory(input_str)
