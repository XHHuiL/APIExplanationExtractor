import scrapy
from ..items import WikiUrlItem


class WikiUrlSpider(scrapy.Spider):
    # scrapy crawl wikiurl
    name = "wikiurl"
    max_depth = 3

    def start_requests(self):
        url = "https://en.wikipedia.org/wiki/Java_(programming_language)"
        # meta used to pass extra parameters
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={'cur_depth': 1}
        )

    @staticmethod
    def is_image(url):
        return url.endswith(".jpg") or url.endswith(".png") or url.endswith(".svg")

    def parse(self, response):
        cur_depth = response.meta['cur_depth']
        item = WikiUrlItem()
        item['url'] = response.url
        yield item
        if cur_depth >= self.max_depth:
            return
        for link in response.xpath('//a/@href'):
            url = response.urljoin(link.get())
            if url.startswith("https://en.wikipedia.org/wiki/") and not self.is_image(url) and not url.find("#") >= 0:
                yield scrapy.Request(url, callback=self.parse, meta={'cur_depth': cur_depth+1})
