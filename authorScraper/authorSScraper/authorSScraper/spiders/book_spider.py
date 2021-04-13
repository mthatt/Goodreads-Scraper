import scrapy
from scrapy.exceptions import CloseSpider

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["goodreads.com"]
    count = 0
    N = 0

    def __init__(self, pages = 0, urlInput=None, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        self.N = pages
        self.urlInput = urlInput

    def start_requests(self):
        urls = [
            self.urlInput,
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.count >= self.N:
            raise CloseSpider(f"Scraped {self.N} items. Eject!")
        self.count += 1
        yield {
            'title': response.css('div.leftContainer div.last.col h1.gr-h1.gr-h1--serif::text')[0].get().strip(),
            'book_url': response.css('div.communityQASignedOutMessage.mediumText a.bookLink::attr(href)').get(),
           #'isbn': response.css('div.buttons div.uitext div.clearFloats div.infoBoxRowItem::text')[1].get().strip(),
            'author_url': response.css('div.bookAuthorProfile__name a::attr(href)')[0].get(),
            'author': response.css('a.authorName>span[itemprop="name"]::text').get(),
            'rating': response.css('div.leftContainer div.uitext.stacked>span[itemprop="ratingValue"]::text').get().strip(),
            'rating_count': response.css('div.leftContainer div.uitext.stacked a.gr-hyperlink>meta::attr(content)')[0].get(),
            'review_count': response.css('div.leftContainer div.uitext.stacked a.gr-hyperlink>meta::attr(content)')[1].get(),
            'image_url': response.css('div.leftContainer div.bookCoverPrimary a>img::attr(src)').get()
        }
        related_books_page = response.css('div.rightContainer div.bigBoxContent.containerWithHeaderContent a.actionLink.right.seeMoreLink::attr(href)').get()
        if related_books_page is not None:
            related_books_page = response.urljoin(related_books_page)
            yield scrapy.Request(related_books_page, callback=self.parseSimilarBooks)

    def parseSimilarBooks(self, response):
        yield {
            'related_books': response.css('div.listWithDividers__item div.objectLockupContent a.gr-h3.gr-h3--serif.gr-h3--noMargin>span[itemprop="name"]::text').extract()[1:],
        }
        related_book_links = response.css('div.listWithDividers__item div.objectLockupContent a.gr-h3.gr-h3--serif.gr-h3::attr(href)').extract()[1:]
        yield from response.follow_all(related_book_links, self.parse)