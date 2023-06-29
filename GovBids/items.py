# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GovbidsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# def splitdate(value):
#     new_value = str((value.split('T',1))[0])
#     return new_value

class BidItem(scrapy.Item):
    Bid= scrapy.Field()
    # print(Bid)
    Bid_No = scrapy.Field()
    Items = scrapy.Field()
    Quantity = scrapy.Field()
    Department = scrapy.Field()
    Startdate = scrapy.Field()
    Enddate = scrapy.Field()
    Document = scrapy.Field()

