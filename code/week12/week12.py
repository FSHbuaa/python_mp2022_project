import requests
import urllib.parse
from bs4 import BeautifulSoup
import os
import pandas as pd
import concurrent.futures 
from threading import Thread, Condition,current_thread

inf_list=[]      #用于储存具体每个歌单的信息（包括url）
inf_plus_list=[] #用来储存在对应歌单url中的信息
song_type = '说唱'
cat = urllib.parse.quote(song_type)

headers1 = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }     #总歌单界面的headers

headers2={
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }     #具体歌单界面的headers

def get_html(url,headers):
    # 构造请求头部
    headers = headers
    # 发送请求，获得响应
    response = requests.get(url=url,headers=headers)
    response.raise_for_status
    response.encoding = response.apparent_encoding
    # 获取响应内容
    html = response.text
    return html

def save_img(url, name):  # 保存图片
    img = requests.get(url)
    f = open(name, 'ab')
    f.write(img.content)
    print(name, '文件保存成功！')
    f.close()

def get_page(cat):
    """
    从主页中获取歌单总页数
    """
    home_page = 0
    url='https://music.163.com/discover/playlist/?order=hot&cat=' + cat + '&limit=35'+'&offset='
    html = get_html(url+str(35*home_page),headers1)
    soup=BeautifulSoup(html,'html.parser')
    txt_page = soup.find('div',{'class':"u-page"})#能够获取页数的信息
    max_page = int(txt_page.text.split('\n')[-3]) #获得该歌单一共有多少页
    return max_page

def get_inf1(page):
    """
    歌单总页面爬取内容
    最后将获取的所有歌单的
    标题、播放量、地址形式id、创建者昵称、id
    添加至全局变量列表
    并将封面图片保存在本地
    """
    url='https://music.163.com/discover/playlist/?order=hot&cat=' + cat + '&limit=35'+'&offset='
    html = get_html(url+str(35*(page-1)),headers1)
    soup=BeautifulSoup(html,'html.parser')
    c=soup.find_all('li')
    folder_path = 'C:\\Users\\LF\\Desktop\\网易云歌单封面\\第'+str(page)+'页封面图片'
    os.makedirs(folder_path, exist_ok=True)
    os.chdir(folder_path)  # 切换路径至上面创建的文件夹
    img_name = 1  # 用来给图片命名
    for item in c:
        try:
            nickname = item.find('a',{'class':"nm nm-icn f-thide s-fc3"})
            name_url=item.find('a',{'class':"tit f-thide s-fc0"})                  #URL信息
            number=int(item.find('span',{'class':'nb'}).text.replace('万','0000')) #播放量的信息
            list1=[
                   name_url['href'],                          #url形式的id信息
                   number,                                    #播放量
                   name_url['title'].replace(u'\xa0', u' '),  #歌单名称
                   nickname['title'],                         #创建者昵称
                   int(name_url['href'].split('=')[-1])]      #id
            inf_list.append(list1)
            img = item.find('img')
            if img is not None:
                url = img['src']
                if url.count('jpg') > 0:
                    save_img(url, str(img_name) + '.jpg')
                elif url.count('png') > 0:
                    save_img(url, str(img_name) + '.png')
                img_name += 1
        except:
            continue
        
def get_inf2(url_id):
    """
    进入具体的某个歌单的url获取信息
    返回id对应歌单的播放了、收藏数、
    创建者昵称、分享数、评论数、歌曲数量、
    歌单名称以及歌单介绍
    添加至全局变量列表
    """
    #print(url_id)
    singleurl='https://music.163.com'+url_id
    singletext=get_html(singleurl,headers=headers2)
    #print(singletext)
    soup=BeautifulSoup(singletext,'html.parser')
    try:
        play_count=eval(soup.find('strong',{'class':'s-fc6'}).text)                                #播放量
        fav=soup.find('a',{'class':'u-btni u-btni-fav'}).i.text.strip('(').strip(')')              #收藏数
        nickname = soup.find('a',{'class':'s-fc7'}).text                                           #创建者昵称
        if('万') in fav:
            fav=eval(fav.replace('万','0000'))
        share=eval(soup.find('a',{'class':'u-btni u-btni-share'}).i.text.strip('(').strip(')'))    #分享数
        comment=eval(soup.find('a',{'data-res-action':'comment'}).i.span.text)                     #评论数
        length=eval(soup.find('span',{'id':'playlist-track-count'}).text)                          #歌曲数量
        name=soup.find('h2',{"class":'f-ff2 f-brk'}).text.replace(u'\xa0', u' ')                   #歌单名称
        tags=soup.find_all('a',{'class':'u-tag'})
        introduction = soup.find('p',{"class":'intr f-brk'}).text.split('\n')
        intr=''
        for i in range(1,len(introduction)):
            intr += introduction[i]
        #print(intr)
        p=len(tags)
        tag1='NA'
        tag2='NA'
        tag3='NA'
        if p>=1:
            tag1=tags[0].text.replace(u'\xa0', u' ')
        if p>=2:
            tag2=tags[1].text.replace(u'\xa0', u' ')            
        if p==3:
            tag3=tags[2].text.replace(u'\xa0', u' ')            
        list1=[name,nickname,play_count,fav,share,comment,length,tag1,tag2,tag3,intr]
        inf_plus_list.append(list1)
        print('解析歌单成功')
    except:
        print('解析歌单失败')
        return

def main():
    max_page = get_page(cat)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for page in range(1,5+1):
        #for page in range(1,max_page+1):
            executor.submit(get_inf1,page)
            #break   #在测试阶段只爬第一页
    pd_inf=pd.DataFrame(inf_list)
    url_lis=list(pd_inf[0])
    #print(url_lis)
    #for i in url_lis:
    #    get_inf2(i)
    #map(get_inf2,url_lis)
    with concurrent.futures.ThreadPoolExecutor() as executor: #多线程处理 
        for id in url_lis:
            executor.submit(get_inf2,id)
    #print(inf_plus_list)
    pd_inf_plus=pd.DataFrame(inf_plus_list)
    title_list=['名称','创建者昵称','播放量','收藏数','分享次数','评论数','歌单数量','tag1','tag2','tag3','介绍']
    c=pd.Series(title_list)
    pd_inf_plus.columns=c
    
    pd_inf_plus.to_csv(r'C:\Users\LF\Desktop\{}.csv'.format(song_type))

if __name__ == '__main__':
    main()