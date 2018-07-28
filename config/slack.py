import os

# Which slack channel to post the listings into.
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', 'immo_test')

# The token that allows us to connect to slack.
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', '')
SLACK_BOT_NAME = os.getenv('SLACK_BOT_NAME', '熊猫')
SLACK_BOT_ICON = os.getenv('SLACK_BOT_ICON', ':panda_face:')
