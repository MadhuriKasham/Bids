# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GovbidsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass



class BidItem(scrapy.Item):
    Bid= scrapy.Field()
    Bid_No = scrapy.Field()
    Items = scrapy.Field()
    Quantity = scrapy.Field()
    Department = scrapy.Field()
    Startdate = scrapy.Field()
    Enddate = scrapy.Field()
    Document = scrapy.Field()

