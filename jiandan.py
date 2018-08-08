import requests
import base64
import re

'''
下载煎蛋网图片
'''

def get_img_hash(page):
    url = 'http://jandan.net/ooxx/page-{}#comments'
    rep = requests.get(url.format(page))
    page = rep.text
    img_hash = re.findall('<span class="img-hash">(.*?)</span>', page)
    return img_hash

def get_img_url(url):
    return 'http:{}'.format(base64.b64decode(url).decode('utf-8'))

url_list=get_img_hash(45)
for i in url_list:
    print(get_img_url(i))


def save_img(url):
    rep=requests.get(url)
    with open('img/'+url.split('/')[-1],'wb')as file:
        file.write(rep.content)
    print(url,'下载完成')

if __name__=="__main__":
    for i in range (1,46):
        hashlist=get_img_hash(i)
        for img in hashlist:
            save_img(get_img_url(img))

