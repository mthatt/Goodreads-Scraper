import scrapy
from scrapy.exceptions import CloseSpider

class AuthorSpider(scrapy.Spider):
    name = "author"
    allowed_domains = ["goodreads.com"]
    count = 0
    N = 0

    def __init__(self, pages = 0, urlInput=None, *args, **kwargs):
        super(AuthorSpider, self).__init__(*args, **kwargs)
        self.N = pages
        self.urlInput = urlInput

    def start_requests(self):
        urls = [
            self.urlInput,
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        author_page = response.css('div.bookAuthorProfile__name a::attr(href)').get()
        if author_page is not None:
            author_page = response.urljoin(author_page)
            yield scrapy.Request(author_page, callback=self.parseAuthorInfo)



    def parseAuthorInfo(self, response):
        if self.count >= self.N:
            raise CloseSpider(f"Scraped {self.N} items. Eject!")
        self.count += 1
        yield {
            'name': response.css('div.rightContainer h1.authorName>span[itemprop="name"]::text').get(),
            'author_url': response.request.url,
            'rating': response.css('span.average::text')[0].get(),
            'rating_count': response.css('span.votes span.value-title::text')[0].get().split()[0],
            'review_count': response.css('span.count span.value-title::text')[0].get().split()[0],
            'image_url': response.css('div.reverseColumnSizes img::attr(src)').get(),
        }

        books_by_author_page = response.css('div.hreview-aggregate a::attr(href)')[0].get()
        if books_by_author_page is not None:
            books_by_author_page = response.urljoin(books_by_author_page)
            yield scrapy.Request(books_by_author_page, callback=self.parseAuthorsBooks)

        related_author_page = response.css('div.hreview-aggregate a::attr(href)')[1].get()
        if related_author_page is not None:
            related_author_page = response.urljoin(related_author_page)
            yield scrapy.Request(related_author_page, callback=self.parseRelatedAuthors)

    def parseAuthorsBooks(selfself, response):
        yield {
            'books': response.css('div.leftContainer a.bookTitle>span[itemprop="name"]::text').extract()
        }

    def parseRelatedAuthors(self, response):
        yield {
            'related_authors': response.css('div.listWithDividers__item div.objectLockupPrimaryContent__main a>span[itemprop="name"]::text').extract()[1:],
        }
        related_author_links = response.css('div.listWithDividers__item div.objectLockupPrimaryContent__main a::attr(href)').extract()[::3]
        print(related_author_links)
        yield from response.follow_all(related_author_links, self.parseAuthorInfo)