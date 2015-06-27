
from twisted.internet import reactor
from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher


class SpiderRunner:
    @staticmethod
    def stop_reactor():
        reactor.stop()

    def __init__(self, spider):
        assert spider is not None
        self.__spider = spider
        self.__crawler = Crawler(Settings())

    def runSpider(self):
        dispatcher.connect(SpiderRunner.stop_reactor,
                           signal=signals.spider_closed)
        crawler = self.__crawler
        crawler.crawl(self.__spider)
        crawler.start()
        log.start()
        log.msg('Starting spider...')
        reactor.run()
        log.msg('Stopped spider.')
