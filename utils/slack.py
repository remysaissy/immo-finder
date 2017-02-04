import settings
from slackclient import SlackClient


class Slack:

    session = SlackClient(settings.SLACK_BOT_TOKEN)

    @staticmethod
    def post_message(o):
        """
        Posts the listing to slack.
        :param offer: A record of the offer.
        """
        desc = "{} – {}m2 - {}€ ({}€/m2) - {} pièces - URL: {}".format(o.title,
                                                                       o.surface, o.price,
                                                                       o.price_per_surface_unit(),
                                                                       o.nb_rooms, o.url)
        Slack.session.api_call("chat.postMessage",
                               channel=settings.SLACK_CHANNEL,
                               text=desc,
                               icon_emoji=settings.SLACK_BOT_ICON,
                               username=settings.SLACK_BOT_NAME)
