import settings
import unicodedata
from urllib.parse import urlparse, urlencode

from app.models.apartment_offer import ApartmentOffer
from app.models.commerce_offer import CommerceOffer
from app.scrapers.base_scraper import BaseScraper


class BienIci(BaseScraper):
    """ BienIci datasource. """

    def __init__(self):
        super().__init__()
        self._base_site_url = 'https://www.bienici.com'
        self._base_search_url = 'recherche/achat'
        # self._base_search_url = 'realEstateAds.json'
        self._page = 1

    def _get_search_url(self):
        location = ','.join(settings.bienici.BIENICI_SEARCH_LOCATION)
        type = ','.join(settings.bienici.BIENICI_SEARCH_TYPE)
        params = dict()
        if settings.filtering.MIN_PRICE > 0:
            params['prix-min'] = settings.filtering.MIN_PRICE
        if settings.filtering.MAX_PRICE > 0:
            params['prix-max'] = settings.filtering.MAX_PRICE
        if settings.filtering.MIN_SIZE > 0:
            params['surface-min'] = settings.filtering.MIN_SIZE
        params['page'] = self._page
        # filters = {
        #     "size": 100,
        #     "from": self._from,
        #     "filterType": "buy",
        #     "newProperty": 'false',
        #     "maxPrice": str(settings.MAX_PRICE),
        #     "minArea": str(settings.MIN_SIZE),
        #     "propertyType": ["flat"],
        #     "sortBy": "publicationDate",
        #     "sortOrder": "desc",
        #     "page": self._page,
        #     "onTheMarket": ['true'],
        #     "showAllModels": 'false',
        #     "zoneIds": ['-7444']
        # }
        # params = {'filters': str(filters).replace(' ', '').replace("'false'", "false").replace("'true'", "true").replace("'", '"')}
        url = '/'.join([self._base_site_url, self._base_search_url, location, type])
        url += ('&', '?')[urlparse(url).query == ''] + urlencode(params)
        return url

    def _has_next_page(self, root):
        tags = root.find_all(lambda tag: tag.has_attr('class') and 'goForward' in tag['class'])
        if len(tags) == 0:
            return False, None
        else:
            self._page += 1
            url = self._get_search_url()
            self.logger.info("Next page {}".format(self._page))
            return True, url

    def _get_offers(self, root):
        return root.find_all(lambda tag: tag.has_attr('class') and 'resultsListContainer' in tag['class'])

    # region fill an offer
    def _get_offer_object(self, r_offer):
        return ApartmentOffer()

    def _is_valid_offer(self, offer, r_offer):
        return r_offer.has_attr('data-id')

    def _prepare_offer_filling(self, offer, r_offer):
        result = None
        url = self.get_details_url(offer, r_offer, None)
        if url is not None:
            offer.details_url = url
            web_page = self._load_web_page(url)
            if web_page is not None:
                res = web_page.find_all(lambda tag: tag.has_attr('class') and 'detailedSheetContainer' in tag['class'])
                if res is not None:
                    result = res[0]
        return result

    def _clean_offer_filling(self, offer, r_offer, payload):
        pass

    def get_details_url(self, offer, r_offer, payload):
        result = None
        res = r_offer.find_all(lambda tag: tag.has_attr('class') and 'detailedSheetLink' in tag['class'])
        if res is not None:
            result = res[0]['href']
        return result

    def get_title(self, offer, r_offer, payload):
        title = None
        res = r_offer.find_all(lambda tag: tag.has_attr('class') and 'descriptionTitle' in tag['class'])
        if res is not None:
            title = res[0].text.strip()
        return title

    def get_description(self, offer, r_offer, payload):
        desc = None
        res = payload.find_all(lambda tag: tag.has_attr('class') and 'descriptionContent' in tag['class'])
        if res is None:
            if payload is not None:
                res = payload.find_all(lambda tag: tag.has_attr('class') and 'descriptionContent' in tag['class'])
        if res is not None:
            desc = res[0].text
            desc = desc.strip()
        return desc

    def get_id(self, offer, r_offer, payload):
        return r_offer['data-id']

    def get_price(self, offer, r_offer, payload):
        price = None
        res = r_offer.find_all(lambda tag: tag.has_attr('class') and 'thePrice' in tag['class'])
        if res is not None:
            price = res[0].text
            price = unicodedata.normalize("NFKD", price).replace(' ','').replace('€','').strip()
        return price

    def __get_surface_from_field(self, field):
        content = field.strip().replace('\t', ' ').replace('\n', ' ')
        surface = None
        high_index = content.find('m²')
        if high_index > -1:
            low_index = content.rfind(' ', 0, high_index)
            if high_index - low_index <= 2:
                low_index = content.rfind(' ', 0, low_index)
            if low_index > -1:
                surface = content[low_index:high_index].strip().replace(',', '.')
                surface = ''.join(c for c in surface if c.isdigit() or c == '.')
        return surface

    def get_surface(self, offer, r_offer, payload):
        surface = self.__get_surface_from_field(offer.title)
        if surface is None:
            surface = self.__get_surface_from_field(offer.description)
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
