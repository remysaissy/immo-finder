import settings
import re

class Filter:
    """ Class used to filter out irrelevant offers. """

    @staticmethod
    def apply(o):
        """
         Applies filters on the offer.
         :param o: The Offer object on which to apply filtering.
         :return True is the offer must be filtered out, False otherwise.
        """
        should_be_filtered = False
        if Filter._filter_by_price(o) \
            or Filter._filter_by_price_per_surface_unit(o) \
            or Filter._filter_by_surface(o) \
            or Filter._filter_by_building_year(o) \
            or Filter._filter_by_postal_code(o) \
            or Filter._filter_by_title(o) \
            or Filter._filter_by_description(o):
            should_be_filtered = True
        return should_be_filtered

    @staticmethod
    def _filter_by_price(o):
        if o.price is None:
            return False
        return o.price > settings.MAX_PRICE

    @staticmethod
    def _filter_by_price_per_surface_unit(o):
        return o.price_per_surface_unit() < settings.MIN_PRICE_PER_SURFACE_UNIT

    @staticmethod
    def _filter_by_surface(o):
        if o.surface is None:
            return False
        return o.surface < settings.MIN_SIZE

    @staticmethod
    def _filter_by_building_year(o):
        if o.building_year is None:
            return False
        return o.building_year > settings.MAX_BUILDING_YEAR

    @staticmethod
    def _filter_by_postal_code(o):
        if o.postal_code is None:
            return False
        found = False
        for district in settings.DISTRICTS:
            if o.postal_code == district:
                found = True
        return not found

    @staticmethod
    def _filter_by_title(o):
        if o.title is not None:
            title = re.findall(r"[\w']+|[.,!?;]", o.title.lower())
            for word in settings.BLACKLISTED_WORDS:
                w = word.lower()
                if w in title:
                    return True
        return False

    @staticmethod
    def _filter_by_description(o):
        if o.description is not None:
            desc = re.findall(r"[\w']+|[.,!?;]", o.description.lower())
            for word in settings.BLACKLISTED_WORDS:
                w = word.lower()
                if w in desc:
                    return True
        return False
