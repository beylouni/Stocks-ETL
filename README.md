<h1 align="center">Welcome to our Stocks-ETL!</h1>
<h4 align="center">By: Eric Naiber & Luciano Farias</h4>

<p align="center">
  <img src="https://user-images.githubusercontent.com/81690594/186323109-acd5aebb-85e6-481a-97cf-d3a46ad4c881.png"/>
</p>

<h4 align="center">Animation by: <a href="https://fga-eps-mds.github.io/2018.2-GamesBI/especificacao/arquitetura.html">GamesBi</a> </h4>
<hr>

## What's about? 🤔
### Learning new technologies and applying what we've learned.

A personal mini project that aims to retrieve stocks market info about chosen companies in _B3_. In first place, the project is to web scrap these infos and send 
them to a _RDS_ database in _AWS_. Further on, some data analysis will be made, developing some 
insights regarding these companies´ stocks behavior.

<hr>

## How it works? 👷
### We used the concept of what is an ETL to guide us on this project.

This project was possible by using webscraping and a crawler to extract the HTML font and then 
RegEx to find the important data. To extract the data we used the website <a href="https://www.investing.com">_investing.com_</a>
followed by it's pages (crawling with Scrapy), and to find the significant data to us, we used RegEx. On the image bellow
it's possible to better understand all the process.

<p align="center">
  <img src="https://user-images.githubusercontent.com/81690594/186456802-1034fe93-91b5-482b-b8cc-2adc7345b027.png"/>
</p>

<h4 align="center">Image by: Eric Naiber</h4>

## How does each process works? ⚙️
### Extract

- Crawler 🕷️
  - Talk about the crawler

### Transform

- Regex 😱
    - Talk about regex.

### Load

- AWS 💸
    - bye bye money 

<hr>

## How to maintain?

bla bla bla Airflow
