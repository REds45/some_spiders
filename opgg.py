import requests
from bs4 import  BeautifulSoup
from pymongo import MongoClient
import re
import time
'''
op.gg 英雄联盟胜率榜
'''

LIST=[ '上单', '打野','中单','下路','辅助']
HEADER={
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

url='http://www.op.gg/champion/statistics'

def get_html():
    source=requests.get(url,headers=HEADER).text
    return source


def save_item(item):
    time_str=time.strftime('%Y-%m-%d',time.localtime())
    client=MongoClient()
    db=client['LOL']
    collection=db['rank_{}'.format(time_str)]
    collection.save(item)


def get_infomation(html):
    #获取胜率，登场率数据
    soup=BeautifulSoup(html,'lxml')
    tags=soup.select('tbody')
    pos=0
    for item in tags:
        lines=item.select('tr')
        for line in lines:
            name=line.select('div.champion-index-table__name')[0].get_text().strip()
            win_rate,pick_rate,tier=line.select('td.champion-index-table__cell.champion-index-table__cell--value')
            tier=re.search('champtier-(.*?).png',tier.select('img')[0].get('src')).group(1)
            tier=0 if tier=='op' else tier
            hero_infomation=dict(name=name,position=LIST[pos],win_rate=win_rate.get_text(),pick_rate=pick_rate.get_text(),tier=tier)
            print(hero_infomation)
            save_item(hero_infomation)
        pos+=1




if __name__=='__main__':
    get_infomation(get_html())