import scrapy
from tqdm import tqdm

pars_bar = tqdm(
    total=628,
    colour='magenta',
    desc='Получаем данные из документации'
)


class PepParseItem(scrapy.Item):
    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
