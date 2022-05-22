import scrapy
from scrapyScraping.items import JobOpeningItem
from urllib.parse import urljoin



class NoFluffSpider(scrapy.Spider):

    def __init__(self, category='', save_format='', **kwargs):
        self.start_urls = [f'https://nofluffjobs.com/pl/{category}']
        super().__init__(**kwargs)

    name = "jobs"
    i = 0
    base_url = 'https://nofluffjobs.com'
    start_urls = [
        #'https://nofluffjobs.com/pl/it-administrator',
        'https://nofluffjobs.com/pl/frontend',
        #'https://nofluffjobs.com/pl/fullstack'
    ]


    def parse(self, response):

        position = []
        company = []

        for job_posting in response.css('.posting-list-item'):
            position = job_posting.css('h3::text').get()
            company = job_posting.css('.posting-title__company::text').get()
            job_url = ''.join([self.base_url, job_posting.css('::attr(href)').get()])

            yield scrapy.Request(url=job_url,
                                 meta={
                                     'company': company,
                                     'position': position,
                                     'job_url': job_url,
                                 },callback=self.parse_job)
        try:
            if 'Next' in response.css('.page-link')[-1].get():
                yield scrapy.Request(url =urljoin(self.base_url, response.css('.page-link').css('::attr(href)')[-1].get()),
                                     callback=self.parse)
        except:
            pass



    def parse_job(self, response):
        department = response.css('.posting-info-row span ::text')[1].get()
        seniority = response.css('common-posting-seniority ::text').get()
        requirements = response.css('common-posting-requirements')[0].css('button ::text').getall()
        try:
            nice_to_have = response.css('common-posting-requirements')[1].css('button ::text').getall()
        except:
            nice_to_have = ''
            print("There are no additional requirements")
        salary = response.css('.salary h4 ::text').get()
        location = response.css('common-posting-locations ::text').getall()
        posting_time = response.css('.posting-time-row ::text').get()
        additional_info = response.css('common-posting-specs p ::text').getall()


        yield JobOpeningItem(
            job_url=response.meta['job_url'],
            position=response.meta['position'],
            company=response.meta['company'],
            seniority = seniority,
            requirements = requirements,
            nice_to_have = nice_to_have,
            salary = salary,
            location = location,
            posting_time = posting_time,
            additional_info = additional_info
        )







