import settings
import unicodedata
from urllib.parse import urlparse, urlencode
from app.scrapers.base_scraper import BaseScraper
from app.models.apartment_offer import ApartmentOffer
from app.models.commerce_offer import CommerceOffer

class SeLoger(BaseScraper):
    """ SeLoger datasource. """

    def __init__(self):
        super().__init__()
        self._base_site_url = 'https://www.seloger.com'
        self._base_search_url = 'list.htm'
        self._page = 1

    def _get_search_url(self):
        params = dict()
        params['qsversion'] = '1.0'
        params['types'] = ','.join(settings.seloger.SELOGER_SEARCH_TYPE)
        params['projects'] = ','.join(settings.seloger.SELOGER_SEARCH_PROJECTS)
        params['natures'] = ','.join(settings.seloger.SELOGER_SEARCH_NATURES)
        params['places'] = "[%s]" % '|'.join(list(map(lambda x: "{cp:%s}" % x, settings.seloger.SELOGER_SEARCH_LOCATION)))
        if settings.filtering.MIN_PRICE > 0 and settings.filtering.MAX_PRICE == 0:
            params['price'] = "{}/NaN".format(settings.filtering.MIN_PRICE)
        elif settings.filtering.MIN_PRICE == 0 and settings.filtering.MAX_PRICE > 0:
            params['price'] = "NaN/{}".format(settings.filtering.MAX_PRICE)
        elif settings.filtering.MIN_PRICE > 0 and settings.filtering.MAX_PRICE > 0:
            params['price'] = "{}/{}".format(settings.filtering.MIN_PRICE, settings.filtering.MAX_PRICE)
        if settings.filtering.MIN_SIZE > 0:
            params['surface'] = "{}/NaN".format(settings.filtering.MIN_SIZE)
        params['LISTING-LISTpg'] = self._page
        url = '/'.join([self._base_site_url, self._base_search_url])
        url += ('&', '?')[urlparse(url).query == ''] + urlencode(params)
        return url

    def _has_next_page(self, root):
        tags = root.find_all(lambda tag: tag.has_attr('class') and tag['class'] == ['pagination-next'])
        if len(tags) == 0:
            return False, None
        else:
            self._page += 1
            url = self._get_search_url()
            self.logger.info("Next page {}".format(self._page))
            return True, url

    def _get_offers(self, root):
        return root.find_all(lambda tag: tag.has_attr('class') and 'c-pa-list' in tag['class'])

    # region fill an offer
    def _get_offer_object(self, r_offer):
        result = None
        res = r_offer.find_all(lambda tag: tag.has_attr('class') and 'c-pa-link' in tag['class'])
        if res is not None and len(res) > 0:
            type = res[0].text.strip()
            if type == 'Local commercial':
                result = CommerceOffer()
            else:
                result = ApartmentOffer()
        return result

    def _is_valid_offer(self, offer, r_offer):
        return True

    def _prepare_offer_filling(self, offer, r_offer):
        result = None
        url = self.get_details_url(offer, r_offer, None)
        if url is not None:
            offer.details_url = url
            web_page = self._load_web_page(url)
            if web_page is not None:
                res = web_page.find_all(lambda tag: tag.has_attr('class') and 'p-detail' in tag['class'])
                if res is not None and len(res) > 0:
                    result = res[0]
        return result

    def _clean_offer_filling(self, offer, r_offer, payload):
        pass

    def get_details_url(self, offer, r_offer, payload):
        result = None
        res = r_offer.find_all(lambda tag: tag.has_attr('class') and 'c-pa-link' in tag['class'])
        if res is not None and len(res) > 0:
            result = res[0]['href']
        return result

    def get_title(self, offer, r_offer, payload):
        title = None
        if payload is not None:
            res = payload.find_all(lambda tag: tag.has_attr('class') and 'detail-title' in tag['class'])
            if res is not None and len(res) > 0:
                title = res[0].text.strip()
        return title

    def get_description(self, offer, r_offer, payload):
        desc = None
        if payload is not None:
            res = payload.find_all(lambda tag: tag.has_attr('id') and tag['id'] == 'js-descriptifBien')
            if res is not None and len(res) > 0:
                desc = res[0].text
                desc = desc.strip()
        return desc

    def get_id(self, offer, r_offer, payload):
        return r_offer['data-publication-id']

    def get_price(self, offer, r_offer, payload):
        price = None
        res = r_offer.find_all(lambda tag: tag.has_attr('class') and 'c-pa-cprice' in tag['class'])
        if res is not None and len(res) > 0:
            price = res[0].text
            price = unicodedata.normalize("NFKD", price).replace(' ','').replace('€','').strip()
        return price

    def get_surface(self, offer, r_offer, payload):
        surface = None
        res = r_offer.find_all(lambda tag: tag.has_attr('class') and 'c-pa-criterion' in tag['class'])
        if res is not None and len(res) > 0:
            criterions = res[0].children
            for criterion in criterions:
                if hasattr(criterion, 'text'):
                    index = criterion.text.find('m²')
                    if index != -1:
                        surface = criterion.text[:index].strip().replace(',', '.')
                        break
        return surface

    def get_created_at(self, offer, r_offer, payload):
        pass

    def get_postal_code(self, offer, r_offer, payload):
        pass

    def get_room_count(self, offer, r_offer, payload):
        pass

    def get_building_year(self, offer, r_offer, payload):
        pass

# endregion

