# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import Compose



class AuthorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    author_url = Field()
    rating = Field()
    rating_count = Field()
    review_count = Field()
    image_url = Field()
    books = Field(output_processsor=Compose(set,list))
    related_authors = Field(output_processsor=Compose(set,list))
