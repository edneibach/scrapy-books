import scrapy
from scrapy.item import Field

class BooksItem(scrapy.Item):
    """A scrapy item with 4 fields for books.toscrape.com - Title, Price, Image URL and Details URL"""

    title = Field()
    price = Field()
    image_url = Field()
    details_url = Field()

class BooksSpider(scrapy.Spider):
    """Scrapy spider that will extract titles, prices, image URLs and detail URLs from all categories from books.toscrape.com"""

    ### Instantiates the spider with a name, allowed domains, and start URL
    ### Also assigns it to the BooksPipeline_EurToUsd, which will convert book prices from EUR to USD
    name = 'books_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    ### Will start by collecting all categories
    ### Then, for each category, it will call a function to scrape books from the category itself
    ### This is a good practice as it adapts to changes in categories in every run, as long as the page layout remains the same
    ### In general, it's best to avoid hard-coding a list of categories or URLs - Instead, getting them dynamically on the go    
    def parse(self, response):
        for category in response.css('.nav-list > li > ul > li > a::attr(href)').getall():
            yield scrapy.Request(url=response.urljoin(category), callback=self.parse_data)
    
    ### Will grab all elements of class .product_pod (which contain the products themselves)
    ### Will then grab and yield info for each element (title, price, image URL, details URL)
    ### If there is a next page, the function is called again in the next page
    ### It's also a good practice to try and make the selectors as subtle (or at least not as nested) as possible (ex: not something like "div > div > div > div > div:last > span")
    def parse_data(self, response):
        books = response.css('.product_pod')
        next_page = response.css('.next > a::attr(href)').extract_first()

        for book in books:
            item = BooksItem()
            item['title'] = book.css('h3 a::attr(title)').extract_first(),
            item['price'] = book.css('.price_color::text').extract_first(),
            item['image_url'] = response.urljoin(book.css('img::attr(src)').extract_first()),
            item['details_url'] = response.urljoin(book.css('h3 a::attr(href)').extract_first())
            yield item

        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_data)    
