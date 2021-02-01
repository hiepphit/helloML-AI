from scrapy import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem


class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["thegioididong.com"]
    start_urls = [
        "https://www.thegioididong.com/dtdd/samsung-galaxy-a50",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//ul[@class="listcomment"]/li')

        for question in questions:
            item = CrawlerItem()

            item['User'] = question.xpath(
                'div[@class="rowuser"]/a/strong/text()').extract_first()
            item['Comment'] = question.xpath(
                'div[@class="question"]/text()').extract_first()
            item['Time'] = question.xpath(
                'div[@class="actionuser"]/a[@class="time"]/text()').extract_first()

            yield item
