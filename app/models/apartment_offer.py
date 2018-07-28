from datetime import datetime

import dateutil.parser

from app.models.base_offer import BaseOffer


class ApartmentOffer(BaseOffer):
    """ DAO representing an offer. """

    def __init__(self):
        super().__init__()
        self.__room_count = None
        self.__building_year = None

    @property
    def room_count(self):
        return self.__room_count

    @room_count.setter
    def room_count(self, value):
        if value is not None:
            self.__room_count = int(value)

    @property
    def building_year(self):
        return self.__building_year

    @building_year.setter
    def building_year(self, value):
        if value is not None:
            self.__building_year = int(value)

    def fill_object(self, datasource, offer, payload):
        super().fill_object(datasource, offer, payload)
        self.room_count = datasource.get_room_count(self, offer, payload)
        self.building_year = datasource.get_building_year(self, offer, payload)
