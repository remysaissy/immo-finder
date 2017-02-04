import xml.etree.ElementTree as ET
from urllib import parse
from urllib.parse import urlparse

import requests

import settings
from datasources import basedatasource
from utils import offer, filter, db

class SeLoger(basedatasource.BaseDataSource):
    """ SeLoger datasource. """

    def _get_details_url(self):
        return 'http://ws.seloger.com/annonceDetail_4.0.xml'

    def _get_details_params(self, o):
        return {'noAudiotel': 1,
                'idAnnonce': o.id}

    def _get_search_url(self):
        return 'http://ws.seloger.com/search_4.0.xml'

    def _get_search_params(self):
        return {
            'surfacemin': settings.MIN_SIZE,
            'getDtCreationMax': 1,
            'idtypebien': 1,
            'cp': 75, # Paris
            'idtt': 2,
            'pxmin': settings.MIN_PRICE,
            'pxmax': settings.MAX_PRICE,
            'naturebien': 1,
            'nbslots': 3
        }

    def _check_next_page_tag(self, root):
        next_page_tag = root.find('pageSuivante')
        if next_page_tag is None:
            return False, None, None
        else:
            components = urlparse(next_page_tag.text)
            url = components.path[1:]
            params = parse.parse_qs(components.query)
            return True, url, params

    def _get_page(self, url, params):
        r = requests.get(url, params=params)
        c = r.content.decode()
        return ET.fromstring(c)

    @staticmethod
    def __get_or_none(obj, key):
        val = obj.find(key)
        if val is not None:
            val = val.text
        return val

    def _build_offers_list(self, root):
        results = []
        r_offers = root.find('annonces').findall('annonce')
        for r_offer in r_offers:
            o = offer.Offer()
            o.id = SeLoger.__get_or_none(r_offer, 'idAnnonce')
            o.created_at = SeLoger.__get_or_none(r_offer, 'dtCreation')
            o.price = SeLoger.__get_or_none(r_offer, 'prix')
            o.surface = SeLoger.__get_or_none(r_offer, 'surface')
            o.postal_code = SeLoger.__get_or_none(r_offer, 'cp')
            o.url = SeLoger.__get_or_none(r_offer, 'permaLien')
            o.nb_rooms = SeLoger.__get_or_none(r_offer, 'nbPiece')
            o.building_year = SeLoger.__get_or_none(r_offer, 'anneeconstruct')

            if db.Offer.is_new_offer(o, self.get_datasource_name()) is False or filter.Filter.apply(o):
                continue

            root_details = self._get_page(self._get_details_url(), self._get_details_params(o))
            o.title = SeLoger.__get_or_none(root_details, 'titre')
            o.description = SeLoger.__get_or_none(root_details, 'descriptif')
            results.append(o)
        return results
