from authorSScraper.authorSScraper.spiders.author_spider import AuthorSpider
from authorSScraper.authorSScraper.spiders.book_spider import BookSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys



class Scraper:
    def __init__(self):
        settings_file_path = 'authorSScraper.authorSScraper.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.numAuthors = int(sys.argv[1])
        self.numBooks = int(sys.argv[2])
        self.urlIn = str(sys.argv[3])
        self.process = CrawlerProcess(get_project_settings())
        self.spiders = [AuthorSpider, BookSpider]

    def run_spiders(self):
        print(self.urlIn)
        self.process.crawl(AuthorSpider, pages=self.numAuthors, urlInput=self.urlIn)
        self.process.crawl(BookSpider, pages=self.numBooks, urlInput=self.urlIn)
        self.process.start()