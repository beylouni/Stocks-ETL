import scrapy
from scrapy.crawler import CrawlerProcess
import datetime
import pandas as pd
import awswrangler as wr

infoList = []


class TopCompanies(scrapy.Spider):
    name = 'top5companies'

    def start_requests(self):
        urls = [
            'https://www.investing.com/equities/apple-computer-inc',
            'https://www.investing.com/equities/microsoft-corp',
            'https://www.investing.com/equities/google-inc-c',
            'https://www.investing.com/equities/amazon-com-inc',
            'https://www.investing.com/equities/tesla-motors'
                ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # page = response.url.split('/')[-1]
        # filename = f'temp/{self.country}/{page}.html'

        xpath_minmax = '//div[@data-test="range-value"]/text()'
        xpath_volume = '//div[@data-test="volume-value"]/text()'
        xpath_currency = '//span[@class="instrument-metadata_text__2iS5i font-bold"]/text()'
        xpath_ticket = '//h1[@class="text-2xl font-semibold instrument-header_title__GTWDv mobile:mb-2"]/text()'

        fullName = response.xpath(xpath_ticket).get()
        start = fullName.index('(') + 1
        end = fullName.index(')')
        ticket = fullName[start:end]

        currency = response.xpath(xpath_currency).get()
        volume = int(response.xpath(xpath_volume).get().replace(',', ''))
        minmax = response.xpath(xpath_minmax).get().split(' - ')
        low = float(minmax[0])
        high = float(minmax[1])

        day = datetime.date.today()

        actualInfo = [day, currency, high, low, volume, ticket]
        infoList.append(actualInfo)


process = CrawlerProcess()
process.crawl(TopCompanies)
process.start()

columnNames = ['date', 'currency', 'high', 'low', 'volume', 'ticket']

df = pd.DataFrame(infoList, columns=columnNames)
df.to_parquet(path='parquets/final.parquet')

wr.s3.to_parquet(
     df=df,
     path="s3://stocks-poatek/stocks-mutable/etl.parquet",
     dataset=True,
     database="stocks-db",
     table="stocks-mutable"
 )
