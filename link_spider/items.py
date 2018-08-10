import scrapy

class ListingItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
