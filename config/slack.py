import os

# Which slack channel to post the listings into.
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '')

# The token that allows us to connect to slack.
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', '')
SLACK_BOT_NAME = os.getenv('SLACK_BOT_NAME', '')
SLACK_BOT_ICON = os.getenv('SLACK_BOT_ICON', '')
