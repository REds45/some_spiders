from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('152.136.158.132', 27017)
db = client.test
pokemon = db.pokemon


rep = requests.get('https://wiki.52poke.com/wiki/种族值列表（第八世代）')
soup = BeautifulSoup(rep.text, 'lxml')
table = soup.select('table.bgl-伽勒尔.bd-伽勒尔 > tbody > tr')
count = 1
for tr in table[1:-1]:
    number_all = tr.select('td:nth-child(1)')[0].text.strip()
    number_v8 = count
    name = tr.select('td:nth-child(3)')[0].text.strip()
    url = tr.select('td:nth-child(3) > a ')[0].get('href')
    count += 1
    data = {
        'number_all': number_all,
        'number_v8': number_v8,
        'name': name,
        'url': 'https://wiki.52poke.com' + url,
        'HP': tr.select('td:nth-child(4)')[0].text.strip(),
        '攻击': tr.select('td:nth-child(5)')[0].text.strip(),
        '防御': tr.select('td:nth-child(6)')[0].text.strip(),
        '特攻': tr.select('td:nth-child(7)')[0].text.strip(),
        '特防': tr.select('td:nth-child(8)')[0].text.strip(),
        '速度': tr.select('td:nth-child(9)')[0].text.strip(),
        '总和': tr.select('td:nth-child(10)')[0].text.strip(),
        '平均值': tr.select('td:nth-child(11)')[0].text.strip(),
    }
    pokemon.insert_one(data)
    print(data)
