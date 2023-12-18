import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def __init__(self):
        self.PART_WITH_NUM = 1
        self.SLIDE_WITH_NAME = 3

    def parse(self, response):
        for pep_doc in response.css((
                'section#numerical-index tbody tr '
                'a.pep.reference.internal::attr(href)')):

            if pep_doc is not None:
                yield response.follow(pep_doc.get(), callback=self.parse_pep)

    def parse_pep(self, response):

        for pep_page in response.css('section#pep-content'):
            row_string = pep_page.css('h1.page-title::text')
            name_value = ' '.join(
                (row_string.get()).split()[self.SLIDE_WITH_NAME:])

            if response.css('h1.page-title span.pre::text').get() is not None:
                name_value = (
                        ' '.join((row_string.get()).split()[
                                 self.SLIDE_WITH_NAME:])
                        + ' ' + response.css('span.pre::text').get())

            data = {
                'number': (
                    row_string.get()).split()[self.PART_WITH_NUM],
                'name': name_value,
                'status': pep_page.css('dl abbr::text').get()
            }

            yield PepParseItem(data)
