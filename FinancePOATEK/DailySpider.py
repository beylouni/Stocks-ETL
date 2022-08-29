import re
from reading import readingCountry as readTXT
from scrapy.crawler import CrawlerProcess
import pandas as pd
import scrapy
import os
from datetime import date

reading_country = readTXT()

"""
All Spiders works almost the same way, read the documentation for more info.
"""

# List for tests
test_list = []


class FinanceSpider(scrapy.Spider):
    name = 'financing_spiderDaily'

    def __init__(self, name_country, **kwargs):
        super().__init__(**kwargs)
        self.country = name_country

    def start_requests(self):
        infos = pd.read_csv(f'csv/{self.country}.csv')

        urls = infos['site_url']
        # urls = ['https://www.investing.com/equities/3r-petroleum-oleo-e-gas-sa-historical-data']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page = response.url.split('/')[-1]
        filename = f'temp/{self.country}/{page}.html'

        html = response.body

        xpath_name = '//h1[@class="text-2xl font-semibold instrument-header_title__GTWDv mobile:mb-2"]/text()'
        xpath_price = '//span[@data-test="instrument-price-last"]/text()'
        xpath_currency = '//span[@class="instrument-metadata_text__2iS5i font-bold"]/text()'
        xpath_maxmin = '//div[@data-test="range-value"]/text()'
        xpath_shift = '//span[@data-test="instrument-price-change-percent"]'
        xpath_volume = '//div[@data-test="volume-value"]/text()'

        full_name = response.xpath(xpath_name).get()
        name = re.sub(r'\((.*?)\)', '', full_name)
        price = float(response.xpath(xpath_price).get())
        currency = response.xpath(xpath_currency).get()

        ticket = re.findall(r'\((.*?)\)', full_name)[0]

        maxmin = response.xpath(xpath_maxmin).get().split(' - ')
        low = float(maxmin[0])
        high = float(maxmin[1])

        shift = response.xpath(xpath_shift).get()
        pattern_shift = r'(?<=-->)\d{1,}\.\d{2}(?=<!--)'
        shift = float(re.findall(pattern_shift, shift)[0])

        volume = int(response.xpath(xpath_volume).get().replace(',', ''))
        today = date.today()

        # 0      1        2          3      4       5      6     7       8
        # NAME | TICKET | CURRENCY | DATE | PRICE | HIGH | LOW | SHIFT | VOLUME

        test_list.append([name, ticket, currency, today, price, high, low, shift, volume])


countries = []
with open(reading_country, 'r') as file:
    countries = file.read().split(',')

for path in countries:
    # Check whether the specified path exists or not
    new_path = f'./temp/{path}'
    isExist = os.path.exists(new_path)

    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(new_path)

process = CrawlerProcess()

for country in countries:
    process.crawl(FinanceSpider, name_country=country)

process.start()

# Just testing
print(f'{"name":70}|{"ticket":10}|{"currency":10}|{"today":10}|{"price":10}|{"max_day":10}|{"min_day":10}|{"shift":10}|{"volume":12}')
for line in test_list:
    name = line[0]
    ticket = line[1]
    currency = line[2]
    today = line[3]
    price = line[4]
    max_day = line[5]
    min_day = line[6]
    shift = line[7]
    volume = line[8]
    # 0      1        2          3      4       5      6     7       8
    # NAME | TICKET | CURRENCY | DATE | PRICE | HIGH | LOW | SHIFT | VOLUME
    print(f'{name:70}|{ticket:10}|{currency:10}|{today}|{price:10}|{max_day:10}|{min_day:10}|{shift:10}|{volume:12}')
