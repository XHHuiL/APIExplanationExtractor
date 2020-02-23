# -*- coding: utf-8 -*-
# A book spider
import scrapy
from ..items import BookItem


# Extends scrapy.Spider to implement custom Spider 
class BookSpider(scrapy.Spider):
    # a unique name for every spider
    name = "books"

    # start urls
    start_urls = ['http://books.toscrape.com/']

    # parse data
    def parse(self, response):
        for item in response.css('article.product_pod'):
            # get book's name and book's price
            book = BookItem()
            book['name'] = item.xpath('./h3/a/@title').get()
            book['price'] = item.css('p.price_color::text').get()
            yield book

            # get next url
            next_url = response.css('ul.pager li.next a::attr(href)').get()
            if next_url:
                next_url = response.urljoin(next_url)
                yield scrapy.Request(next_url, callback=self.parse)
