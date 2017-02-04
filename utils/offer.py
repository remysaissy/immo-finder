import dateutil.parser
from datetime import datetime


class Offer(object):
    """ DAO representing an offer. This DAO is not meant to be persisted in DB, only for In-Memory processing. """

    def __init__(self):
        self._id = None
        self._created_at = None
        self._price = None
        self._surface = None
        self._title = None
        self._postal_code = None
        self._description = None
        self._nb_rooms = None
        self._url = None
        self._building_year = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is not None:
            self._id = str(value)

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if value is not None:
            if isinstance(value, int):
                self._created_at = datetime.fromtimestamp(value)
            elif isinstance(value, str) and value.isdigit():
                self._created_at = datetime.fromtimestamp(int(value))
            else:
                self._created_at = dateutil.parser.parse(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is not None:
            self._price = int(float(value))

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        if value is not None:
            self._surface = int(float(value))

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value is not None:
            self._title = str(value).lower()

    @property
    def postal_code(self):
        return self._postal_code

    @postal_code.setter
    def postal_code(self, value):
        if value is not None:
            self._postal_code = int(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is not None:
            self._description = str(value).lower()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if value is not None:
            self._url = value

    @property
    def nb_rooms(self):
        return self._nb_rooms

    @nb_rooms.setter
    def nb_rooms(self, value):
        if value is not None:
            self._nb_rooms = int(value)

    @property
    def building_year(self):
        return self._building_year

    @building_year.setter
    def building_year(self, value):
        if value is not None:
            self._building_year = int(value)

    def price_per_surface_unit(self):
        return int(self.price / self.surface)
