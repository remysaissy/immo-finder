import time

import logging
from app.utils import logger as log
from app.datasources import pap, seloger


def timed_job():
    log.init_logging()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.info("{}: Starting scrape cycle".format(time.ctime()))
    pap.Pap().run()
    # bienici.BienIci().run()
    seloger.SeLoger().run()
    logger.info("{}: Successfully finished scraping".format(time.ctime()))

timed_job()
