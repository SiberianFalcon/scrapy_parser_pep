import inspect

import scrapy

try:
    from pep_parse.items import PepItem
except ModuleNotFoundError:
    raise AssertionError('Не найден файл `items.py`')
except ImportError as exc:
    raise AssertionError(f'Не найден класс `PepItem` в файле {exc.name}')


def test_items_fields():
    assert inspect.isclass(PepItem), (
        '`PepItem` должен быть классом.'
    )
    assert issubclass(PepItem, scrapy.Item), (
        '`PepItems` должен наследоваться от `scrapy.Item`'
    )
    fields = ['name', 'number', 'status']
    for field in fields:
        assert field in list(PepItem.fields.keys()), (
            f'В `PepItem` не хватает атрибута `{field}`'
        )
