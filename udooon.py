#coding: utf-8
import scrapelib
from bs4 import BeautifulSoup
import udooonlib as udnlib
from pandas import Series, DataFrame
import pandas as pd

data = []

# 市町村コードに変換
city_code = udnlib.city_kanji2code("さぬき")

# データ取得
s = scrapelib.Scraper(requests_per_minute=10)
ret = s.get('http://tabelog.com/kagawa/' + city_code + '/rstLst/?vs=1&sk=%25E3%2581%2586%25E3%2581%25A9%25E3%2582%2593&lid=hd_search1&vac_net=&svt=1900&svps=2&hfc=1&RdoCosTp=2&LstCos=0&LstCosT=0&LstRev=0&LstSitu=0&Cat=RC&LstCat=RC01&LstCatD=RC0104&LstCatSD=RC010402&sw=')
soup = BeautifulSoup(ret.text, "html.parser")
omises = soup.find_all("li", class_="js-cassette js-rstlst-cassete list-rst is-blocklink js-bookmark")


def get_omise_info(omises):
    for omise in omises:
        omise_tsuika = {}
        #お店の名前
        namae = omise.find("a", class_="list-rst__rst-name-target js-click-rdlog")
        omise_tsuika["name"] = namae.string
    
        #合計評価ポイント
        point_strong = omise.find_all("span", class_="list-rst__rating-val tb-rating__val tb-rating__val--strong")
        if len(point_strong) != 0:
            if(point_strong[0].string != "-"):
                omise_tsuika["point_gokei"] = float(point_strong[0].string)

        #昼/夜の評価ポイント
        hiruyoru = omise.find_all("p", class_="list-rst__rating-time tb-rating tb-rating--sm")
        if(len(hiruyoru) != 0):
            yoru = hiruyoru[0].find_all("span", class_="list-rst__rating-val tb-rating__val tb-rating__val--strong")
            hiru = hiruyoru[1].find_all("span", class_="list-rst__rating-val tb-rating__val tb-rating__val--strong")
            if(yoru[0].string != "-"):
                omise_tsuika["point_yoru"] = float(yoru[0].string)
            if(hiru[0].string != "-"):
                omise_tsuika["point_hiru"] = float(hiru[0].string)

        
        #コメント件数
        comment = omise.find_all("em", class_="list-rst__rvw-count-num")
        if len(comment) != 0:
            omise_tsuika["comment"] = int(comment[0].string)

        #昼/夜の予算
        yosan = omise.find_all("li", class_="list-rst__budget-item tb-rating tb-rating--sm")
        if(len(yosan) != 0):
            yosan_yoru = yosan[0].find_all("span", class_="list-rst__budget-val tb-rating__val")
            yosan_hiru = yosan[1].find_all("span", class_="list-rst__budget-val tb-rating__val")
            omise_tsuika["yoru_yosan"] = yosan_yoru[0].string
            omise_tsuika["hiru_yosan"] = yosan_hiru[0].string
        
        #席数等々
        other_info = omise.find("p", class_="list-rst__table-data")
        #取得した座席数などの情報を文字列に
        other_info = str(other_info.string)
        #ゴミを取り除く
        other_info = other_info.replace('\n', '')
        other_info = other_info.replace(' ', '')
        #配列の形に分解
        other_info = other_info.split("／")
        seki_kazu = ''
        koshitsu = ''
        kemuri = ''
        for i in other_info:
            if(i.find("席") != -1):
                seki_kazu = i
                seki_kazu = seki_kazu.replace("席", "")
                omise_tsuika["seki"] = int(seki_kazu)
            if(i.find("個") != -1):
                omise_tsuika["koshitsu"] = i
            if(i.find("煙") != -1):
                omise_tsuika["kemuri"] = i
        data.append(omise_tsuika)

get_omise_info(omises)

#次ページのリンク取得
next = soup.find("a", class_="page-move__target page-move__target--next")
while next!=None :
    next_page = next.get("href")
    r2 = s.get(next_page)
    soup = BeautifulSoup(r2.text, "html.parser")
    omises = soup.find_all("li", class_="js-cassette js-rstlst-cassete list-rst is-blocklink js-bookmark")
    
    get_omise_info(omises)
    
    #次ページのリンク取得
    next = soup.find("a", class_="page-move__target page-move__target--next")


df = DataFrame(data, 
              columns=['name', 
                       'point_gokei', 'point_hiru', 'point_yoru',
                      'hiru_yosan','yoru_yosan',
                      'seki','kemuri','koshitsu',
                      'comment'])
df.sort_values(by="point_gokei",ascending=False) 
