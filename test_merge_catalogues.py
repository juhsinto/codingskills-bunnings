from merge_catalogues import *
import unittest
import os
import pandas as pd
import warnings

class TestMergeCatalogues(unittest.TestCase):
    def test_files_exist(self):
        self.assertTrue(os.path.isfile("input/catalogA.csv"))
        self.assertTrue(os.path.isfile("input/catalogB.csv"))
        self.assertTrue(os.path.isfile("input/barcodesA.csv"))
        self.assertTrue(os.path.isfile("input/barcodesB.csv"))

    def test_getBarcodes(self):
        # these files are used by getBarcodes ; and are required as a global variable
        bar_A = pd.read_csv("input/barcodesA.csv")
        bar_B = pd.read_csv("input/barcodesB.csv")

        # assert that the result of an existing barcode results in barcodes
        self.assertTrue(len(getBarcodes('647-vyk-317')) > 0)

        # assert negative test
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            getBarcodes('random-sku-doesntexist')
            # Verify some things
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "No barcode found for SKU!" in str(w[-1].message)

    def test_barcode_exists(self):
        list_one = ['test', 'one', 'two']
        list_two = ['test', 'fat', 'cat']

        self.assertTrue(barcode_exists(list_one, list_two))
        list_three = ['thincat', 'fatcat']

        self.assertFalse(barcode_exists(list_three, list_two))
