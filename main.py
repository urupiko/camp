import requests
import sqlite3
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

BASE_URL= "https://www3.yadosys.com/reserve/ja/room/calendar/147/ehejfcebejdheigbgihfgpdn/all"


def get_next5month(is_debug, cur):
    if is_debug is True:
        this_soup = BeautifulSoup(open('page1.html',encoding = 'utf-8'),'html.parser')
        next_soup = BeautifulSoup(open('page2.html',encoding = 'utf-8'),'html.parser')
    else:
        r = requests.get(BASE_URL)
        this_soup = BeautifulSoup(r.text, "html.parser")
        next_month = datetime.now() + relativedelta(months=3)
        r = requests.get('%s/%d%02d01' % (BASE_URL, next_month.year, next_month.month))
        next_soup = BeautifulSoup(r.text, "html.parser")
    
    box_list = ['boxLeft', 'boxCenter', 'boxRight']
    for box_name in box_list:
        box= this_soup.find('div', class_=box_name)
        store_month(box, cur)
    for box_name in box_list:
        box= next_soup.find('div', class_=box_name)
        store_month(box, cur)

def store_month(box, cur):
    h4_month = box.find('h4')
    # print(h4_month.get_text())
    match = re.search(r'(\d{4})(\d+)月', h4_month.get_text())
    y = match.group(1)
    m = match.group(2)

    # テーブの解析
    mat = []
    table = box.find('table')
    tbody = table.find('tbody')  # tbodyタグを探す
    trs = tbody.find_all('tr')  # tbodyからtrタグを探す
    for tr in trs:
        for td in tr.find_all('td'):  # trタグからtdタグを探す
            if td.text == '\xa0':
                continue
            # 1満のようになるので、文字列を分解する
            # mat.append(td.text)
            match = re.search(r'(\d+)(\S)', td.text)
            d = match.group(1)
            status = match.group(2)
            if status != '-':
                cur.execute('INSERT INTO 予約状況(日付, 状況) values(?, ?)', (f'{y}-{m:0>2}-{d:0>2}', status))
                # print(f'{y}-{m}-{d} {status}')

    # print(mat)


dbname = 'main.db'
conn = sqlite3.connect(dbname)

# 
# 時刻 日付 ステータス
# CREATE TABLE 予約状況(状況ID INTEGER PRIMARY KEY AUTOINCREMENT, チェック日時 datetime, 日付 date, 状況 STRING);
cur = conn.cursor()
# time = datetime.now().strftime("%B %d, %Y %I:%M%p")
# cur.execute('INSERT INTO 予約状況(日付, 状況) values(?, ?)', (str(datetime.date), 'hoge'))

cur.execute('CREATE TABLE IF NOT EXISTS 予約状況(ID INTEGER PRIMARY KEY AUTOINCREMENT, チェック日時 DEFAULT CURRENT_TIMESTAMP, 日付 TEXT, 状況 TEXT)')
conn.commit()

get_next5month(True, cur)
conn.commit()

conn.close()