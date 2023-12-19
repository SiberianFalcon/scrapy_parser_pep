import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    PART_WITH_NUM = 1
    SLIDE_WITH_NAME = 1
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
        page_title = response.css('title::text')

        data = {
                'number': (page_title.get()).split(' ', 2)[1],
                'name': (page_title.get()).split(' ', 3)[3][:-18],
                'status': response.css('dl abbr::text').get()
        }

        yield PepParseItem(data)
