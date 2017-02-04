import sys
import traceback
import time
from utils import slack, filter, db


class BaseDataSource(object):
    """ Abstract class for implementing a datasource. """

    def _get_search_url(self):
        """
         The search url of the datasource
         :return string
        """
        NotImplementedError("Class {} doesn't implement aMethod()".format(self.__class__.__name__))

    def _get_search_params(self):
        """
        :return: search parameters for the datasource
        """
        NotImplementedError("Class {} doesn't implement aMethod()".format(self.__class__.__name__))

    def _check_next_page_tag(self, root):
        """
            Check if there is a next page tag and returns it parameters.
             :returns has_next_page(bool),url(string),params(dict)
        """
        NotImplementedError("Class {} doesn't implement aMethod()".format(self.__class__.__name__))

    def _get_page(self, url, params):
        """
         Retrieves results and returns a ready to use return object
         :return Response object ready to use by other methods.
        """
        NotImplementedError("Class {} doesn't implement aMethod()".format(self.__class__.__name__))

    def _build_offers_list(self, root):
        """
         Builds a list of offers
         :return list(Offer)
        """
        NotImplementedError("Class {} doesn't implement aMethod()".format(self.__class__.__name__))

    def _next_page(self):
        """ Retrieve the next page of results. This method must yield each page.
          :return list[Offer]: A list of Offer objects.
        """
        has_next = True
        url = self._get_search_url()
        params = self._get_search_params()

        while has_next:
            root = self._get_page(url, params)
            has_next, url, params = self._check_next_page_tag(root)
            yield self._build_offers_list(root)

    def get_datasource_name(self):
        """ Returns the datasource's name. """
        return self.__class__.__name__

    def run(self):
        """ Runs the datasource. """
        print("{}: Retrieving offers from {}...".format(time.ctime(), self.get_datasource_name()))
        try:
            total_count = 0
            for offers in self._next_page():
                for o in offers:
                    if db.Offer.is_new_offer(o, self.get_datasource_name()) and filter.Filter.apply(o) is False:
                        db.Offer.persist_offer(o, self.get_datasource_name())
                        slack.Slack.post_message(o)
                        total_count += 1
        except Exception as exc:
            print("Error with the scraping:", sys.exc_info()[0])
            traceback.print_exc()
        else:
            print("{}: Got {} results from {}".format(time.ctime(), total_count, self.get_datasource_name()))

