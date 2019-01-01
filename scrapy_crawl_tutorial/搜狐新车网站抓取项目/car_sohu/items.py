# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#sohu
class SohunewcarItem(scrapy.Item):
    grabtime=scrapy.Field()
    website = scrapy.Field()
    status=scrapy.Field()
    url = scrapy.Field()
    brandid = scrapy.Field()
    brandname = scrapy.Field()
    familyid = scrapy.Field()
    familyname = scrapy.Field()
    trimid = scrapy.Field()
    trimname = scrapy.Field()
    trimgear = scrapy.Field()
    trimdisp = scrapy.Field()
    trimyear = scrapy.Field()



