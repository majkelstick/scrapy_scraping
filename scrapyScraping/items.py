# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class IMDBItem(scrapy.Item):
    title = scrapy.Field()
    page_url = scrapy.Field()
    release_year = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    description = scrapy.Field()
    genres = scrapy.Field()

class JobOpeningItem(scrapy.Item):
    job_url = scrapy.Field()
    position = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    seniority = scrapy.Field()
    department = scrapy.Field()
    location = scrapy.Field()
    requirements = scrapy.Field()
    nice_to_have = scrapy.Field()
    additional_info = scrapy.Field()
    posting_time = scrapy.Field()

    def __repr__(self):
        """only print out title after exiting the Pipeline"""
        return repr({"position": self['position']})

