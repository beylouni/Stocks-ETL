import pandas as pd
import requests
import bs4
import re

url = 'https://br.investing.com/equities/brazil'
pattern = r'<a href="/equities(.*?)>'

html = requests.get(url).content
soup = str(bs4.BeautifulSoup(html, 'lxml'))

matches = re.findall(pattern, soup)


def parsing(line):
    if '?' in line:
        return re.sub(r'\?(.*?) ', ' ', line)
    else:
        return line


listed_matches = filter(lambda line: 'title' in line, matches)
listed_matches = map(lambda line: parsing(line), listed_matches)
listed_matches = map(lambda line: line.replace('"', '').split(' title='), listed_matches)

df = pd.DataFrame(listed_matches, columns=["site_url", "name"])

url_part = 'https://www.investing.com/equities'
end_url = '-historical-data'
df['site_url'] = url_part + df['site_url'] + end_url

df.to_csv('csv/brazil.csv')
