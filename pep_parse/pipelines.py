import csv
from datetime import datetime
from .settings import BASE_DIR





class PepParsePipeline:
    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.result_list = dict()
        self.count = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.result_list[item['status']] = self.result_list.get(item[
            'status'], 0) + 1
        return item

    def close_spider(self, spider):
        date = datetime.today().strftime(
            f'{self.results_dir}/status_summary_%Y-%m-%d_%H-%M-%S.csv')

        with open(date, 'a', encoding='utf-8') as f:
            f = csv.writer(f, dialect='unix', delimiter=',')
            f.writerow(('Статус', 'Кол-во'))

        for k, v in self.result_list.items():
            with open(date, 'a', encoding='utf-8') \
                    as f:
                f = csv.writer(f, dialect='unix', delimiter=',')
                f.writerow((k, v))

        with open(date, 'a', encoding='utf-8') as f:
            f = csv.writer(f, dialect='unix', delimiter=',')
            f.writerow(('Total', sum(self.result_list.values())))
