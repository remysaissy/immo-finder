import time
import logging
from app.utils import logger as log
from app.scrapers import *

def timed_job():
    log.init_logging()
    logger = logging.getLogger()
    logger.info("{}: Starting scrape cycle".format(time.ctime()))
    # bienici.BienIci().scrape()
    pap.Pap().scrape()
    seloger.SeLoger().scrape()
    logger.info("{}: Successfully finished scraping".format(time.ctime()))

timed_job()
