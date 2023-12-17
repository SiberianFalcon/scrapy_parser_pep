import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for pep_doc in response.css((
                'section#numerical-index tbody tr '
                'a.pep.reference.internal::attr(href)')):

            if pep_doc is not None:
                yield response.follow(pep_doc.get(), callback=self.parse_pep)

    def parse_pep(self, response):
        for pep_page in response.css('section#pep-content'):
            data = {
                'number': (
                    pep_page.css('h1.page-title::text').get()).split()[1],
                'name': (pep_page.css(
                    'h1.page-title::text').get()).split('–')[1],
                'status': pep_page.css('dl abbr::text').get()
            }

            yield PepParseItem(data)
