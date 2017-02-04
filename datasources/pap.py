import json
import time

import requests

import settings
from datasources import basedatasource
from utils import offer, db, filter


class Pap(basedatasource.BaseDataSource):
    """ Pap datasource. """

    HEADERS = {'X-Device-Gsf': settings.PAP_DEVICE_GSF}

    def __init__(self):
        self._page = 1
        self._nb_pages = 0

    def _get_search_url(self):
        return 'http://ws.pap.fr/immobilier/annonces'

    def _get_search_params(self):
        return {
            'recherche[produit]': 'vente',
            'recherche[prix][min]': settings.MIN_PRICE,
            'recherche[prix][max]': settings.MAX_PRICE,
            'recherche[surface][min]': settings.MIN_SIZE,
            'recherche[typesbien][]': 'appartement',
            'recherche[geo][ids][]': 439,               # Geocode for Paris
            'order': 'date-desc',
            'recherche[last_check]': int(time.time()) - settings.SLEEP_INTERVAL,
            'size': 200,
            'page': self._page
        }

    def _check_next_page_tag(self, root):
        self._nb_pages = int(root['nb_pages'])
        self._page += 1
        if self._page > self._nb_pages:
            return False, None, None
        else:
            url = self._get_search_url()
            params = self._get_search_params()
            return True, url, params

    def _get_page(self, url, params):
        r = requests.get(url, params=params, headers=Pap.HEADERS)
        c = r.content.decode()
        return json.loads(c)

    def _build_offers_list(self, root):
        results = []
        r_offers = root['_embedded']['annonce']
        for r_offer in r_offers:
            o = offer.Offer()
            o.id = r_offer['id']
            o.price = r_offer['prix']
            o.surface = r_offer['surface']
            o.url = r_offer['_links']['desktop']['href']
            if 'nb_pieces' in r_offer:
                o.nb_rooms = r_offer['nb_pieces']
            if db.Offer.is_new_offer(o, self.get_datasource_name()) is False or filter.Filter.apply(o):
                continue
            details = self._get_page(r_offer['_links']['self']['href'], None)
            o.description = details['texte']
            o.title = details['_embedded']['place'][0]['title']
            o.created_at = details['date_classement']
            # o.postal_code = r_offer['postalCode']
            results.append(o)
        return results
