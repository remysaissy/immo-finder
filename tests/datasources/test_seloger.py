import unittest

import xml.etree.ElementTree as ET

class SeLogerTestCase(unittest.TestCase):
    """ Unit Tests for seloger.py """

    def setUp(self):
        tree = ET.parse('seloger_annonce.xml')
        self.offer_root = tree.getroot()

    # def test_


if __name__ == '__main__':
    unittest.main()