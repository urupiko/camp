from bs4 import BeautifulSoup

import requests
url = "https://www3.yadosys.com/reserve/ja/room/calendar/147/ehejfcebejdheigbgihfgpdn/all"

# 今月を含む5ヶ月を探査する
# 

# ほんとうは月を指定したい
# url = "https://www3.yadosys.com/reserve/ja/room/calendar/147/ehejfcebejdheigbgihfgpdn/all/20230801"

# r = requests.get(url)
# soup = BeautifulSoup(r.text, "html.parser")
soup = BeautifulSoup(open('page2.html',encoding = 'utf-8'),'html.parser')
print(soup.title)

boxCenter = soup.find('div', class_='boxCenter')
h4_month = boxCenter.find('h4')
print(h4_month.get_text())

# 時刻 日付 ステータス

# テーブの解析
mat = []
table = boxCenter.find('table')
tbody = table.find('tbody')  # tbodyタグを探す
trs = tbody.find_all('tr')  # tbodyからtrタグを探す
for tr in trs:
    for td in tr.find_all('td'):  # trタグからtdタグを探す
        if td.text == '\xa0':
            continue
        mat.append(td.text)

print(mat)