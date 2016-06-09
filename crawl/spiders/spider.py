from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawl.items import CrawlItem

class StockSpider(BaseSpider):
    name = "stock"
    allowed_domains = ["finance.daum.net"]
    start_urls = [
        "http://finance.daum.net/quote/all.daum?type=U&stype=P",
        "http://finance.daum.net/quote/all.daum?type=U&stype=Q",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        sites = hxs.select('//table[@class="gTable clr"]')

        items = []

        for site in sites:
            item = CrawlItem()
            href = site.select('//td[@class="txt"]/a/@href').extract()
            item['stock_id'] = [i.split('=')[1] for i in href]
            item['stock_name'] = site.select('//td[@class="txt"]/a//text()').extract()
            items.append(item)

        return items