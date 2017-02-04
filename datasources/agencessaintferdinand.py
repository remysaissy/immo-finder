from bs4 import BeautifulSoup
import requests

import settings
from datasources import basedatasource
from utils import offer, db, filter


class AgencesSaintFerdinand(basedatasource.BaseDataSource):
    """ Agences Saint Ferdinand datasource. """

    def __init__(self):
        self._page = 1
        self._nb_pages = 0

    def _get_search_url(self):
        return 'http://www.agencessaintferdinand.com/advanced-search/'

    def _get_search_params(self):
        return {
            'filter_search_action[]': 'vente',
            'advanced_city': '',
            'price_low': settings.MIN_PRICE,
            'price_max': settings.MAX_PRICE
        }

    def _check_next_page_tag(self, root):
        return False, None, None

    def _get_page(self, url, params={}):
        r = requests.get(url, params=params)
        c = r.content.decode()
        return BeautifulSoup(c)

    def _build_offers_list(self, root):
        results = []
        r_offers = root.find_all('div', class_='listing_wrapper')
        for r_offer in r_offers:
            o = offer.Offer()
            o.url = r_offer.find('h4').find('a').get('href')
            details = self._get_page(o.url)
            o.id = details.find('div', id='propertyid_display').text.split(':')[1].strip()
            o.description = details.find('div', id='description').text.strip()
            o.title = r_offer.find('a').text.strip()
            entries = details.find_all('div', class_='listing_detail')
            for entry in entries:
                kv = entry.text.split(':')
                if kv[0].lower() == 'zip':
                    o.postal_code = kv[1].strip()
                elif kv[0].lower() == 'année construction':
                    o.building_year = kv[1].strip()
                elif kv[0].lower() == 'prix':
                    o.price = kv[1].replace('€','').replace('.','').strip()
                elif kv[0].lower() == 'surface logement':
                    o.surface = kv[1].replace('m2', '').strip()
                elif kv[0].lower() == 'pièces':
                    o.nb_rooms = kv[1].strip()
            if db.Offer.is_new_offer(o, self.get_datasource_name()) is False or filter.Filter.apply(o):
                continue
            results.append(o)
        return results
