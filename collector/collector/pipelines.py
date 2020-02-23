# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.exceptions import DropItem
import spacy


# the pipeline used to filter newline character
class FilterNewlineCharacterPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        data = item['description']
        # replace '\n' by ''
        item['description'] = data.replace("\n", "")
        return item


class StripPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        data = item['description']
        # strip
        item['description'] = data.strip()
        return item


class FilterMultiSpacesPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        data = item['description']
        # replace multi spaces by one
        item['description'] = re.sub(r' +', ' ', data)
        return item


nlp = spacy.load("en_core_web_sm")


class SyntaxAnalysisPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        result = ""
        data = item['description']
        para = nlp(data)
        # divide paragraph into sentences
        for sent in para.sents:
            # dependency parsing
            desc = nlp(sent.text)
            hasSubject = False
            hasObject = False
            for token in desc:
                dep = token.dep_
                if (dep == 'expl') or (dep == 'csubj') or (dep == 'csubjpass') or (dep == 'nsubj') or (
                        dep == 'nsubjpass'):
                    hasSubject = True
                elif (dep == 'attr') or (dep == 'dobj') or (dep == 'pobj'):
                    hasObject = True
            if hasSubject and hasObject:
                result += sent.text
        if result == "":
            raise DropItem("illegal description")
        item['description'] = result
        return item
