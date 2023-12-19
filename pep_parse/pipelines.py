import csv
from datetime import datetime

from .settings import BASE_DIR


class PepParsePipeline:
    DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'

    def __init__(self):
        self.RESULT_DIR = BASE_DIR / 'results'

    def open_spider(self, spider):
        self.result_list = dict()

    def process_item(self, item, spider):
        self.result_list[
            item['status']] = self.result_list.get(item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        file_name = datetime.today().strftime(
            f'{self.RESULT_DIR}/status_summary_{self.DATE_FORMAT}.csv')

        with open(file_name, 'a', encoding='utf-8') as f:
            f = csv.writer(f, dialect='unix', delimiter=',')
            f.writerow(('Статус', 'Кол-во'))
            f.writerows([(k, v) for k, v in self.result_list.items()])
            f.writerow(('Total', sum(self.result_list.values())))
