import scrapy
from ..items import JavaDescriptionItem


class JavaApiSpider(scrapy.Spider):
    # scrapy crawl stackoverflow -o stackoverflow.json
    name = "stackoverflow"
    start_urls = ["https://stackoverflow.com/questions/tagged/java"]
    max_count = 10000
    count = 0

    def parse(self, response):
        # select only question summary with more than 0 answers
        for question_summary in response.xpath('//*[@id="questions"]//div[@class="question-summary"]'):
            answer_num = (int)(question_summary.xpath('./div[1]/div[1]/div[2]/strong/text()').get())
            # if number of answers bigger than 0, crawl corresponding answers
            if answer_num > 0:
                answers_url = question_summary.xpath('./div[2]/h3/a/@href').get()
                answers_url = response.urljoin(answers_url)
                yield scrapy.Request(answers_url, callback=self.parse_answer)
                if self.count > self.max_count:
                    return

        # the url of next page
        next_page_url = response.xpath('//*[@id="mainbar"]/div[@class="pager fl"]/a[@rel="next"]/@href').get()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(next_page_url, callback=self.parse)
    
    # extract answer
    def parse_answer(self, response):
        for answer in response.xpath('//div[contains(@class, "answer")]//div[@class="post-text"]/p/text()'):
            item = JavaDescriptionItem()
            item["description"] = answer.get()
            yield item
            self.count += 1
