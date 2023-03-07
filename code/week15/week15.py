import gevent
from gevent import monkey
monkey.patch_all()
#将第三方库标记为IO非阻塞

import pymongo
import urllib.parse
import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO
import pandas as pd

save_img_flag = False

def get_html(url):
    '''
    获取网址
    '''
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
    }
    response = requests.get(url = url,headers = headers)   #向服务器请求数据，获得对应html
    html = response.text   
    #print(html)
    return html
    
def get_id(page):
    '''
    生产者
    1. 获得歌单的id⭐
    2. 保存图片
    '''
    #这里的page是以网址上的为准，也就是35的倍数
    #for page in range(0,1505,35):
    #print(page)
    urlid_lis = []   #歌单的id列表
    cat = urllib.parse.quote('欧美')   #category choose 
    url = 'https://music.163.com/discover/playlist/?order=hot&cat='+cat+'&limit=35&offset='+str(page)
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')   #从html中提取所有的数据
    inf = soup.find_all('li')   #把所有信息保存下来
    #print(inf)
    for item in inf:
        id_inf = item.find('a',{'class':'msk'})
        if id_inf is not None:
            urlid_lis.append(id_inf['href'])   #保存id
    if save_img_flag == True:   #保存图片
        pic = 1
        path = 'F:\\现代程序设计技术\\week 12\\网易云歌单封面\\第'+str(int(page/35)+1)+'页封面图片'
        os.makedirs(path, exist_ok=True)
        os.chdir(path)  # 切换路径至上面创建的文件夹
        for item in inf:
            img = item.find('img',{'class':'j-flag'})
            if img is not None:
                save_img(img['src'],str(pic))
                pic += 1
        print(f'第{int(page/35)+1}页图片保存完成')
        #print(urlid_lis)
    return urlid_lis

def save_img(img,pic):
    '''
    保存图片函数
    '''
    res = requests.get(img)
    image = Image.open(BytesIO(res.content))
    try:
        image.save(pic + '.jpg')
    except:
        image.save(pic + '.png')
        
def get_inf(id):
    '''
    获取某歌单的全部信息，包括：
    歌单标题、创建者id、创建者昵称、介绍、
    歌曲数量、播放量、添加到播放列表次数、分享次数、评论数
    ID，title，text，author，date，mp3_path（对mp3文件，在表中只存储路径即可）
    ，related_articles。其中ID可在url中获取，title，author，date，related_articles等内容可在数据页面内找到。
    '''
    url = 'https://music.163.com' + str(id)
    text = get_html(url)
    soup = BeautifulSoup(text,'html.parser')
    try:
        id_0 = id.split('=')[-1]
        title = soup.find('h2',{"class":'f-ff2 f-brk'}).text.replace(u'\xa0', u' ')          #歌单标题
        author = soup.find('a',{'class':'s-fc7'}).text                                       #创建者
        text = soup.find('p',{"class":'intr f-brk'}).text.replace('\n','')[3:]        #文本
        date = soup.find('span',{"class":'time s-fc4'}).text.replace(u'\xa0', u' ')[:-3]        #日期
        #mp3_path由于未下载歌曲不进行实现
        inf = soup.find_all('li')
        #print(inf)
        related_articles=''
        for item in inf:
            title_inf = item.find('a',{'class':'sname f-fs1 s-fc0'})
            if title_inf is not None:
                title_inf=title_inf['title']
                if len(related_articles) == 0:
                    related_articles += title_inf
                else:
                    related_articles += ','+title_inf
        list = [id_0,title,text,author,date,related_articles]
        print('成功保存歌单数据')
        return list
    except:
        pass
    
    
def main():
    jobs_id=[]
    for page in range(0,35 * 1,35):  #共1505，暂时只爬取前10页
        jobs_id.append(gevent.spawn(get_id,page))
    gevent.joinall(jobs_id)
    url_lis=[]
    for job in jobs_id:
        for url in job.value:
            url_lis.append(url)
    print(url_lis)
    jobs_inf=[]
    for url in url_lis:
        jobs_inf.append(gevent.spawn(get_inf,url))
    gevent.joinall(jobs_inf)
    inf=[]
    for job in jobs_inf:
        if job.value:             #有些url读取信息失败没有返回值
            inf.append(job.value)
    texts=[]
    for list in inf:
        dic={}
        col = ['ID','title','text','author','date','related_articles']
        for i in range(len(col)):
            dic[col[i]] = list[i]
        texts.append(dic)
    print('load %d lines' % len(texts))
    client = pymongo.MongoClient('localhost',27017)
    db=client.yrq
    collection=db.baobei
    result=collection.insert_many(texts)
    print(result)
    client.close()
        
    
        
if __name__ == '__main__':
    main()