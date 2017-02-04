import json

import requests

import settings
from datasources import basedatasource
from utils import offer


class BienIci(basedatasource.BaseDataSource):
    """ BienIci datasource. """

    def __init__(self):
        self._cookies = None
        self._from = 0
        self._page = 1
        self._total = -1

    def _get_search_url(self):
        return 'https://www.bienici.com/realEstateAds.json'

    def _get_search_params(self):
        filters = {
            "size": 100,
            "from": self._from,
            "filterType": "buy",
            "newProperty": 'false',
            "maxPrice": str(settings.MAX_PRICE),
            "minArea": str(settings.MIN_SIZE),
            "propertyType": ["flat"],
            "sortBy": "publicationDate",
            "sortOrder": "desc",
            "page": self._page,
            "onTheMarket": ['true'],
            "showAllModels": 'false',
            "zoneIds": ['-7444']
        }
        return {'filters': str(filters).replace(' ', '').replace("'false'", "false").replace("'true'", "true").replace("'", '"')}

    def _check_next_page_tag(self, root):
        self._total = int(root['total'])
        self._page += 1
        self._from += int(root['perPage'])
        if self._from >= self._total:
            return False, None, None
        else:
            url = self._get_search_url()
            params = self._get_search_params()
            return True, url, params

    def _get_page(self, url, params):
        r = requests.get(url,
                         params=params,
                         cookies=self._cookies)
        self._cookies = r.cookies.copy()
        c = r.content.decode()
        return json.loads(c)

    def _build_offers_list(self, root):
        results = []
        r_offers = root['realEstateAds']
        for r_offer in r_offers:
            o = offer.Offer()
            o.id = r_offer['id']
            o.created_at = r_offer['publicationDate']
            o.price = r_offer['price']
            if 'surfaceArea' in r_offer:
                o.surface = r_offer['surfaceArea']
            if 'postalCode' in r_offer:
                o.postal_code = r_offer['postalCode']
            if 'roomsQuantity' in r_offer:
                o.nb_rooms = r_offer['roomsQuantity']
            o.url = "https://www.bienici.com/annonce/vente/{}/appartement/{}pieces/{}".format(r_offer['city'].lower().replace(' ', '-'),
                                                                                      o.nb_rooms, o.id)
            if 'title' in r_offer:
                o.title = r_offer['title']
            else:
                o.title = r_offer['city']
            o.description = r_offer['description']
            results.append(o)
        return results
