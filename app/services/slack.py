from slackclient import SlackClient
from app.models.apartment_offer import ApartmentOffer
from app.models.commerce_offer import CommerceOffer
import settings

import logging

class Slack:

    session = SlackClient(settings.slack.SLACK_BOT_TOKEN)
    logger = logging.getLogger()

    @staticmethod
    def post_message(o):
        """
        Posts the listing to slack.
        :param offer: A record of the offer.
        """
        if isinstance(o, ApartmentOffer):
            desc = "Appartment - {} – {}m2 - {}€ ({}€/m2) - {} pièces - URL: {}".format(o.title,
                                                                           o.surface, o.price,
                                                                           o.price_per_surface_unit(),
                                                                           o.room_count, o.details_url)
        elif isinstance(o, CommerceOffer):
            desc = "Murs de commerce - {} – {}m2 - {}€ ({}€/m2) - URL: {}".format(o.title,
                                                                                    o.surface, o.price,
                                                                                    o.price_per_surface_unit(),
                                                                                    o.details_url)
        Slack.session.api_call("chat.postMessage",
                               channel=settings.slack.SLACK_CHANNEL,
                               text=desc,
                               icon_emoji=settings.slack.SLACK_BOT_ICON,
                               username=settings.slack.SLACK_BOT_NAME)
