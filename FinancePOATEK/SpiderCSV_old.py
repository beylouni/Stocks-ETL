import re
from reading import readingCountry as readTXT
from scrapy.crawler import CrawlerProcess
import pandas as pd
import scrapy
import os

reading_country = readTXT()

"""
All Spiders works almost the same way, read the documentation for more info.
"""


class FinanceSpider(scrapy.Spider):
    name = 'financing_spiderCSV'

    def __init__(self, name_country, **kwargs):
        super().__init__(**kwargs)
        self.country = name_country

    def start_requests(self):
        infos = pd.read_csv(f'csv/{self.country}.csv')

        urls = infos['site_url']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page = response.url.split('/')[-1]
        filename = f'temp/{self.country}/{page}.html'

        html = response.body

        xpath_table = '//table[@data-test="historical-data-table"]'
        table = response.xpath(xpath_table).get()

        table_pd = pd.read_html(table)
        table_pd[0].to_parquet(filename + '.parquet')


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
