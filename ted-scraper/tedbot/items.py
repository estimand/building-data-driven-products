import scrapy


class Speaker(scrapy.Item):
    id = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    description = scrapy.Field()
    bio = scrapy.Field()


class Talk(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    event = scrapy.Field()
    duration = scrapy.Field()
    timings = scrapy.Field()
    filmed_at = scrapy.Field()
    published_at = scrapy.Field()
    speakers = scrapy.Field()
    tags = scrapy.Field()
    viewed = scrapy.Field()
    ratings = scrapy.Field()
    external_links = scrapy.Field()
    transcript = scrapy.Field()
