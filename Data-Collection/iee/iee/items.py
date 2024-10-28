# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class IeeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    authors = scrapy.Field()
    country = scrapy.Field()
    abstract_ = scrapy.Field()
    date_pub = scrapy.Field()
    journal = scrapy.Field()
    topic = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()