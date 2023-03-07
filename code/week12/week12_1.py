import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures 
from multiprocessing.dummy import Pool as pool

limit=10000#热门歌单播放量筛选下限
headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
headers1={
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
finallist=[]
url_list=[]
count=0
LABEL='轻音乐'

def getHTMLText(url,headers): #通用的获取网站内容的框架
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "网络解析错误"

def get_url(cat,depth):#获取首页该分类下面的歌单url，形成url_list
    #depth=1
    start_url='https://music.163.com/discover/playlist/?order=hot&cat='+cat
    for i in range(depth):
        try:
            url=start_url+'&limit=35'+'&offset='+str(35*(i+1))
            html=getHTMLText(url,headers)
            parse_main(html)
        except:
            print('失败')
            continue

def parse_main(html):#解析单个url
    soup=BeautifulSoup(html,'html.parser')
    c=soup.find_all('li')
    for unit in c:
        try:
            name_url=unit.find('a',{'class':"tit f-thide s-fc0"})#m这里有URL，名字的信息
            print(name_url['href'])
            number=eval(unit.find('span',{'class':'nb'}).text.replace('万','0000'))#这里获取的是播放量的信息,用于初步筛选
            print(unit.find('span',{'class':'nb'}).text.replace('万','0000'))
            list1=[name_url['title'].replace(u'\xa0', u' '),number,name_url['href']]
            url_list.append(list1)
        except:
            continue


def parse_single(listid):#进入歌单内部解析，获取播放量，收藏量，标签等信息
    #print(count)
    #print('\0')
    print(listid)
    singleurl='https://music.163.com'+listid
    #print(singleurl)
    #print('\0')
    singletext=getHTMLText(singleurl,headers=headers1)
    #print("**")
    soup=BeautifulSoup(singletext,'html.parser')
    try:
        play_count=eval(soup.find('strong',{'class':'s-fc6'}).text)
        fav=soup.find('a',{'class':'u-btni u-btni-fav'}).i.text.strip('(').strip(')')
        if('万') in fav:
            fav=eval(fav.replace('万','0000'))
        share=eval(soup.find('a',{'class':'u-btni u-btni-share'}).i.text.strip('(').strip(')'))
        comment=eval(soup.find('a',{'data-res-action':'comment'}).i.span.text)
        length=eval(soup.find('span',{'id':'playlist-track-count'}).text)
        date=soup.find('span',{'class':'time s-fc4'}).text[:10]
        name=soup.find('h2',{"class":'f-ff2 f-brk'}).text.replace(u'\xa0', u' ')     
        tags=soup.find_all('a',{'class':'u-tag'})
        p=len(tags)
        tag1='nan'
        tag2='nan'
        tag3='nan'
        if p>=1:
            tag1=tags[0].text.replace(u'\xa0', u' ')
        if p>=2:
            tag2=tags[1].text.replace(u'\xa0', u' ')            
        if p==3:
            tag3=tags[2].text.replace(u'\xa0', u' ')            
        list1=[name,date,play_count,fav,share,comment,length,tag1,tag2,tag3]
        finallist.append(list1)
        print('解析第歌单成功')
    except:
        print('解析第歌单失败')
        return

def main(type,depth=38):
    get_url(type,depth=depth)
    print("歌单列表获取完成")
    print(url_list)
    a=pd.DataFrame(url_list)
    b=list(a[2])
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(parse_single,b)
    #多线程  
    print(finallist)
    a=pd.DataFrame(finallist)
    b=pd.DataFrame(url_list)
    title_list=['名称','创建日期','播放次数','收藏量','转发量','评论数','歌单长度','tag1','tag2','tag3']
    c=pd.Series(title_list)
    a.columns=c
    a.to_excel(r'C:\Users\LF\Desktop\{}.xlsx'.format(type))
    #数据输出到Excel

if __name__ == '__main__':
    main(LABEL,depth=1)
# depth就是总共爬取多少页的，打开网站可以发现每页上有30多个，总共有38页。