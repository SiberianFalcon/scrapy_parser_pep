import scrapy
from tqdm import tqdm
from ..items import PepParseItem


pars_bar = tqdm(
    total=628,
    colour='magenta',
    desc='Получаем данные из документации'
)


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
            pars_bar.update(1)
            yield PepParseItem(data)


