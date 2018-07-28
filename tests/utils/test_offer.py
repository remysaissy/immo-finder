import unittest

from datetime import datetime
import app.models.offer


class OfferTestCase(unittest.TestCase):
    """ Unit Tests for offer.py """

    def test_id(self):
        o = app.models.offer.Offer()
        o.id = '42'
        self.assertEqual(o.id, '42')

    def test_created_at_with_datetime(self):
        o = app.models.offer.Offer()
        o.created_at = '2016-09-17T06:41:00'
        self.assertEqual(o.created_at, datetime(2016, 9, 17, 6, 41))

    def test_created_at_with_ts(self):
        o = app.models.offer.Offer()
        o.created_at = 1473942600
        self.assertEqual(o.created_at, datetime(2016, 9, 15, 14, 30))

        o.created_at = '1473942600'
        self.assertEqual(o.created_at, datetime(2016, 9, 15, 14, 30))

    def test_price(self):
        o = app.models.offer.Offer()
        o.price = '42'
        self.assertEqual(o.price, 42)

    def test_surface(self):
        o = app.models.offer.Offer()
        o.surface = '42'
        self.assertEqual(o.surface, 42)

    def test_title(self):
        o = app.models.offer.Offer()
        o.title = 'Foo bar text'
        self.assertEqual(o.title, 'foo bar text')

    def test_postal_code(self):
        o = app.models.offer.Offer()
        o.postal_code = '42'
        self.assertEqual(o.postal_code, 42)

    def test_description(self):
        o = app.models.offer.Offer()
        o.description = 'Foo bar text'
        self.assertEqual(o.description, 'foo bar text')

    def test_url(self):
        o = app.models.offer.Offer()
        o.url = 'http://foo.bar/42'
        self.assertEqual(o.url, 'http://foo.bar/42')

    def test_nb_rooms(self):
        o = app.models.offer.Offer()
        o.nb_rooms = '2'
        self.assertEqual(o.nb_rooms, 2)

    def test_building_year(self):
        o = app.models.offer.Offer()
        o.building_year = '1870'
        self.assertEqual(o.building_year, 1870)

    def test_price_per_surface_unit(self):
        o = app.models.offer.Offer()
        o.price = 830000
        o.surface = 82
        self.assertEqual(o.price_per_surface_unit(), int(o.price/o.surface))

if __name__ == '__main__':
    unittest.main()
