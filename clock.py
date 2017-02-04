import time

from datasources import pap, seloger, bienici, agencessaintferdinand


def timed_job():
    print("{}: Starting scrape cycle".format(time.ctime()))
    agencessaintferdinand.AgencesSaintFerdinand().run()
    pap.Pap().run()
    bienici.BienIci().run()
    seloger.SeLoger().run()
    print("{}: Successfully finished scraping".format(time.ctime()))

timed_job()
