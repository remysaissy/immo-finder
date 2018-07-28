import settings
from app.datasources.base_datasource import BaseDataSource
from app.models.apartment_offer import ApartmentOffer
from app.models.commerce_offer import CommerceOffer


class Pap(BaseDataSource):
    """ Pap datasource. """

    def __init__(self):
        super().__init__()
        self._base_site_url = 'https://www.pap.fr'
        self._base_search_url = 'annonce/vente'
        self._page = 1

    def _get_search_url(self):
        if settings.filtering.MIN_PRICE > 0 and settings.filtering.MAX_PRICE == 0:
            price_range = "a-partir-de-{}-euros".format(settings.filtering.MIN_SIZE)
        elif settings.filtering.MIN_PRICE == 0 and settings.filtering.MAX_PRICE > 0:
            price_range = "jusqu-a-{}-euros".format(settings.filtering.MAX_PRICE)
        elif settings.filtering.MIN_PRICE > 0 and settings.filtering.MAX_PRICE > 0:
            price_range = "entre-{}-et-{}-euros".format(settings.filtering.MIN_PRICE, settings.filtering.MAX_PRICE)
        else:
            price_range = ''
        if settings.filtering.MIN_SIZE > 0:
            min_size = "a-partir-de-{}-m2".format(settings.filtering.MIN_SIZE)
        else:
            min_size = ''
        search_type = '-'.join(settings.pap.PAP_SEARCH_TYPE)
        site_base = '/'.join([self._base_site_url, self._base_search_url])
        search_url =  '-'.join([site_base, search_type, settings.pap.PAP_SEARCH_LOCATION, price_range, min_size, str(self._page)])
        return search_url, None

    def _has_next_page(self, root):
        tags = root.find_all(lambda tag: tag.has_attr('class') and tag['class'] == ['next'])
        if len(tags) == 0:
            return False, None, None
        else:
            self._page += 1
            url, params = self._get_search_url()
            self.logger.info("Next page {}".format(self._page))
            return True, url, params

    def _get_offers(self, root):
        return root.find_all(lambda tag: tag.has_attr('class') and tag['class'] == ['item-title'])

# region fill an offer
    def _get_offer_object(self, r_offer):
        url = '/'.join([self._base_site_url, r_offer['href']])
        if 'local-commercial' in url or 'local-d-activite' in url:
            return CommerceOffer()
        else:
            return ApartmentOffer()

    def _is_valid_offer(self, offer, r_offer):
        return r_offer.has_attr('name')

    def _prepare_offer_filling(self, offer, r_offer):
        url = '/'.join([self._base_site_url, r_offer['href']])
        offer.details_url = url
        web_page = self._load_web_page(url, None)
        if web_page is not None:
            return web_page.find_all(lambda tag: tag.has_attr('class') and tag['class'] == ['details-item'])[0]
        else:
            return None

    def _clean_offer_filling(self, offer, r_offer, payload):
        pass

    def get_details_url(self, offer, r_offer, payload):
        url = '/'.join([self._base_site_url, r_offer['href']])
        return url

    def get_title(self, offer, r_offer, payload):
        title = payload.find_all(lambda tag: tag.has_attr('class') and tag['class'] == ['h1'])[0].text.strip()
        return title

    def get_description(self, offer, r_offer, payload):
        desc = payload.find_all(lambda tag: tag.has_attr('class') and 'item-description' in  tag['class'])[0].find_all('p')[0].text
        desc = desc.strip()
        return desc

    def get_id(self, offer, r_offer, payload):
        return r_offer['name']

    def get_price(self, offer, r_offer, payload):
        price = ''.join(c for c in r_offer.find_all(lambda tag: tag.has_attr('class') and tag['class'] == ['item-price'])[0].text.replace('.','') if c in ['0','1','2','3','4','5','6','7','8','9','0'])
        price = price.strip()
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
