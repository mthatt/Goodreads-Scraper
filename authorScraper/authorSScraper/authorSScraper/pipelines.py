# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from pymongo import MongoClient
from itemadapter import ItemAdapter

class AuthorsscraperPipeline:
    def __init__(self):
        client = pymongo.MongoClient(
            "mongodb+srv://dbUser242:123qwe4r@cluster0.2qwnu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['goodreads']
        self.collection = db['goodreads_info']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
