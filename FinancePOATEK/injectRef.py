from reading import readingCountry as readTXT
import pandas as pd
import requests
import bs4
import re

# Importing the right file.
reading_country = readTXT()


def startUrlsByCountry():
    """
    You can watch step by step on the code by following the 'num' step.
    The objective of this function is:

    1 - read a .txt file and get the input like -> (directory)/(country/region).txt

    2 - on this input file you have to have all country names separated by commas -> brazil,argentina,... ->
    spaces will generate an error

    3 - join the country name and the link from investing.com -> https://br.investing.com/equities/(country) -> and
    then downloading the page

    4 - find the right pattern and the link on the text from the page then clean data with map/filter and a
    parsing function (written in the code).
    OBS:
        4.1 - I'm using regex here to learn a new lib, but you can easily use xpath for this work
        4.2 - An Spider from scrapy is way more efficient than request+bs4, but again, my goal here is to learn

    5 - Generate a dataframe containing: index, url for the stock page, stock name -> all stocks from a country
    will be converted to a CSV and stored at csv directory.

    """

    def parsing(line):
        """
        Function to clean the data from required output.
        """
        if '?' in line:
            return re.sub(r'\?(.*?) ', ' ', line)
        else:
            return line

    # Step 1
    countries = []
    with open(reading_country, 'r') as file:
        countries = file.read().split(',')

    # Step 2
    for url_country in countries:
        try:
            # Step 3
            url = f'https://br.investing.com/equities/{url_country}'
            pattern = r'<a href="/equities(.*?)>'

            # Step 4
            html = requests.get(url).content
            soup = str(bs4.BeautifulSoup(html, 'lxml'))

            matches = re.findall(pattern, soup)

            listed_matches = filter(lambda line: 'title' in line, matches)
            listed_matches = map(lambda line: parsing(line), listed_matches)
            listed_matches = map(lambda line: line.replace('"', '').split(' title='), listed_matches)

            # Step 5
            df = pd.DataFrame(listed_matches, columns=["site_url", "name"])

            url_part = 'https://www.investing.com/equities'
            end_url = '-historical-data'
            df['site_url'] = url_part + df['site_url'] + end_url

            df.to_csv(f'csv/{url_country}.csv')

        except:
            # Not the best way to use an except, I'm going to fix latter (if I remember)
            print(f'Fail to scrape {url_country}')


startUrlsByCountry()
