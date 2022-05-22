import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapyScraping.items import IMDBItem

class IMDBSpider(CrawlSpider):
    name = 'imdb'
    rules = (
        # extract links at the bottom of the page. note that there are 'Prev' and 'Next'
        # links, so a bit of additional filtering is needed
        Rule(LinkExtractor(restrict_xpaths=('//*[@class="desc"]/a')),
            process_links=lambda links: filter(lambda l: 'Next' in l.text, links),
            callback='parse_page',
            follow=True),
    )

    def __init__(self, start=None, end=None, *args, **kwargs):
      super(IMDBSpider, self).__init__(*args, **kwargs)
      self.start_year = int(start) if start else 1920
      self.end_year = int(end) if end else 1920

    # generate start_urls dynamically
    def start_requests(self):
        for year in range(self.start_year, self.end_year+1):
            yield scrapy.Request('http://www.imdb.com/search/title?year=%d,%d&title_type=feature&sort=moviemeter,asc' % (year, year))

    def parse_page(self, response):
        for movie in response.css('.lister-item-header a'):
            item = IMDBItem()
            item['title'] = movie.css('a::text').get()
            # (you will need to change it in items.py as well)
            item['page_url']= "http://imdb.com"+movie.css('a::attr(href)').get()
            request = scrapy.Request(item['page_url'], callback=self.parseMovieDetails)
            request.meta['item'] = item
            yield request




    def parseMovieDetails(self, response):
        item = response.meta['item']
        item['release_year'] = response.css('ul a::text')[0].get()
        try:
            item['rating'] = response.css('div[data-testid="hero-rating-bar__aggregate-rating__score"] span::text ')[0].get()
        except:
            item['rating'] = ''
        item['writer'] =response.css(
            '.ipc-inline-list__item[role="presentation"] a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text'
            )[1].getall()

        item['director'] = response.css(
            '.ipc-inline-list__item[role="presentation"] a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text'
            )[1].getall()
        item['description'] = response.css('p[data-testid="plot"] span::text').get()
        item['genres'] = response.css('div[data-testid="genres"] a ul li::text').getall()
        print(item)
        yield item