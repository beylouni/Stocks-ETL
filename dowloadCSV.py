import pandas as pd
import requests
import bs4
import re
import time

start_time_all = time.time()

infos = pd.read_csv('csv/brazil.csv')

names = infos['name']
urls = infos['site_url']


def matchPrice(url):
    html = str(bs4.BeautifulSoup(requests.get(url).content, 'lxml'))
    pattern = r'"instrument-price-last">(.*?)</span>'
    return re.findall(pattern, str(html))[0]


"""for i in range(len(infos)):

    start_time = time.time()
    
    if '?' in urls[i]:
        pattern = r'\?(.*?)-'
        text = urls[i]
        infos['site_url'][i] = re.sub(pattern, '-', text)[0]

    price = matchPrice(urls[i])

    print(f'{names[i]:50s}|'
          f'R$ {price:10}|'
          f'Time: {(time.time() - start_time):.3f}s'
          f'|{urls[i]:90} |{i}')"""


