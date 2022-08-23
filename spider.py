from scrapy.crawler import CrawlerProcess
import pandas as pd
import scrapy
from os.path import exists

infos = pd.read_csv('csv/brazil.csv')

names = infos['name']
urls_all = infos['site_url']


class InvestingSpider(scrapy.Spider):
    name = 'investing_spider'

    def start_requests(self):
        urls = urls_all

        for i, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        i = 0
        while exists(f'temp/investing{i}.html'):
            i += 1
        html_file = f'temp/investing{i}.html'
        with open(html_file, 'wb') as fout:
            fout.write(response.body)


process = CrawlerProcess()
process.crawl(InvestingSpider)
process.start()