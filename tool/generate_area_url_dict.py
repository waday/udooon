#coding: utf-8
import scrapelib
from bs4 import BeautifulSoup
import prefkanji2roma as pk2r
s = scrapelib.Scraper(requests_per_minute=10)
ret = s.get('http://tabelog.com/kagawa/')
soup = BeautifulSoup(ret.text, "html.parser")
areas = soup.find_all("li", class_="list-balloon__list-col")

area_url_dict = {} 
for area in areas:
        # stringに<!--¥n-->が含まれているので削除
        area_name = str(area.a).replace('<!--\n-->','')
        area_soup = BeautifulSoup(area_name, "html.parser")
        url = area_soup.a.get('href').replace('A', 'C').split('/')[4]
        area_name = area_soup.string.strip()
        area_url_dict[area_name] = url

print(area_url_dict)
