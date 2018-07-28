from datetime import datetime

import dateutil.parser


class BaseOffer(object):

    def __init__(self):
        self.__id = None
        self.__details_url = None
        self.__description = None
        self.__title = None
        self.__price = None
        self.__surface = None
        self.__created_at = None
        self.__postal_code = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None:
            self.__id = str(value)

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        if value is not None:
            if isinstance(value, int):
                self.__created_at = datetime.fromtimestamp(value)
            elif isinstance(value, str) and value.isdigit():
                self.__created_at = datetime.fromtimestamp(int(value))
            else:
                self.__created_at = dateutil.parser.parse(value)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value is not None:
            self.__price = int(float(value))

    @property
    def surface(self):
        return self.__surface

    @surface.setter
    def surface(self, value):
        if value is not None:
            self.__surface = int(float(value))

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if value is not None:
            self.__title = str(value).lower()

    @property
    def postal_code(self):
        return self.__postal_code

    @postal_code.setter
    def postal_code(self, value):
        if value is not None:
            self.__postal_code = int(value)

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if value is not None:
            self.__description = str(value).lower()

    @property
    def details_url(self):
        return self.__details_url

    @details_url.setter
    def details_url(self, value):
        if value is not None:
            self.__details_url = value

    def price_per_surface_unit(self):
        return int(self.price / self.surface)

    def fill_object(self, datasource, offer, payload):
        self.details_url = datasource.get_details_url(self, offer, payload)
        self.description = datasource.get_description(self, offer, payload)
        self.title = datasource.get_title(self, offer, payload)
        self.id = datasource.get_id(self, offer, payload)
        self.price = datasource.get_price(self, offer, payload)
        self.surface = datasource.get_surface(self, offer, payload)
        self.created_at = datasource.get_created_at(self, offer, payload)
        self.postal_code = datasource.get_postal_code(self, offer, payload)

