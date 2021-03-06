import scrapy
from scrapy.exceptions import CloseSpider
from ..items import WikiParaItem


max_depth = 3
max_num = 500000
cur_num = 0


class WikiParaSpider(scrapy.Spider):
    # scrapy crawl wikipara
    name = "wikipara"

    def start_requests(self):
        url = "https://en.wikipedia.org/wiki/Wiki"
        # meta used to pass extra parameters
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={'cur_depth': 1}
        )

    @staticmethod
    def is_image(url):
        return url.endswith(".jpg") or url.endswith(".png") or url.endswith(".svg")

    @staticmethod
    def is_entity(url):
        return url.find("#") < 0 and url.find(":") < 0

    def parse(self, response):
        global cur_num
        # //*[@id="mw-content-text"]/div/p[3]
        for para in response.xpath('//*[@id="mw-content-text"]//p'):
            item = WikiParaItem()
            item['text'] = para.xpath('string(.)').get()
            yield item
            cur_num += 1
            if cur_num > max_num:
                raise CloseSpider('enough data')
        cur_depth = response.meta['cur_depth']
        if cur_depth >= max_depth:
            return
        for link in response.xpath('//*[@id="bodyContent"]//a/@href'):
            href = link.get()
            url = response.urljoin(href)
            if url.startswith("https://en.wikipedia.org/wiki/") and not self.is_image(href) and self.is_entity(href):
                yield scrapy.Request(url, callback=self.parse, meta={'cur_depth': cur_depth+1})
