import numpy as np
import jieba
import re
from matplotlib import pyplot as plt

#文件名用作全局变量
filename_0=r'C:\Users\LF\Desktop\weibo.txt\weibo.txt'
filename_0_test=r'C:\Users\LF\Desktop\weibo.txt\test_weibo.txt'
filename_anger=r'C:\Users\LF\Desktop\emotion_lexicon\anger.txt'
filename_disgust=r'C:\Users\LF\Desktop\emotion_lexicon\disgust.txt'
filename_fear=r'C:\Users\LF\Desktop\emotion_lexicon\fear.txt'
filename_joy=r'C:\Users\LF\Desktop\emotion_lexicon\joy.txt'
filename_sadness=r'C:\Users\LF\Desktop\emotion_lexicon\sadness.txt'
filename_emotions=[filename_anger,filename_disgust,filename_fear,filename_joy,filename_sadness]
EMO=['anger','disgust','fear','joy','sadness']
TIMEMODE=['week','hour','month']


def fread_document(filename) -> list:
    """
    按行读入txt文件并返回列表
    ->返回一维列表
    :filename:原始文档目录
    """
    print("----------正在导入数据----------")
    f=open(filename,encoding='UTF-8')
    line = f.readline().strip() #读取第一行,不用读入列表
    txt=[]
    while line:  # 直到读取完文件
        line = f.readline().strip()  # 读取一行文件，包括换行符
        txt.append(line)
    f.close()  # 关闭文件
    if txt[-1]=='':
        txt.pop()
    print("----------数据导入完成----------")
    return txt

def fdelete_repetition_txt(txt) -> list:
    """
    删除列表中的重复元素
    ->返回与原始列表相同结构的列表
    :txt:需删除重复元素的列表
    """
    if len(txt) != len(set(txt)):
        print("有重复微博")
        txt = [x for x in set(txt)]
    return txt

def fcut_txt(txt,n) -> list:
    """
    将按行读入的数据按'\t'切割
    ->返回column=4的二维列表
    :txt:按行读入的数据列表
    :n:txt的长度
    """
    data=[]
    for i in range(n):
        s=txt[i].split("\t")
        if len(s)==4:
            data.append(s)
    return data

def fdelete_url_data(data,n) -> list:
    """
    删除每条微博后相同的url地址
    ->返回与data相同的column=4的二位列表
    :data:切割好的二维列表
    :n:二维列表长度
    """
    sentence=[]   #专门用来储存微博内容
    #根据字符串格式切割
    for i in range(n):
        #print(data[i][1])
        sentence.append(data[i][1].rsplit(' ',1)[0])
    ##print(sentence)
    return sentence

def fclean_sentence(sentence,n) -> list:
    """
    使用正则表达式对文本降噪
    ->返回与sentence相同的一维列表
    :sentence:
    :n:列表长度
    """
    for i in range(n):
        sentence[i] = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)"," ",sentence[i])  # 去除正文中的@和回复/转发中的用户名
        sentence[i] = re.sub(r'[\S]+\.(cn|net|com|org|info|edu|gov|uk|de|ca|jp|fr|au|us|ru|ch|it|nel|se|no|es|mil)[\S]*\s?','',sentence[i])# 去除网址
        sentence[i] = re.sub(r"\s+", " ", sentence[i]) # 合并正文中过多的空格
    return sentence

def faddword(filename_emotions):
    """
    jieba添加自定义字典
    """
    print("----------正在添加情绪词----------")
    for i in filename_emotions:
        jieba.load_userdict(i)

def fdic_emotion(filename_emotions,data,sentence,n):
    """
    闭包函数返回情绪，时间，地址列表函数
    ->函数名
    :filename_emotions:情绪地址列表
    :data:column=4的全信息列表
    :sentence:处理后的文本字符
    :n:列表长度
    """
    emodict = []
    for i in filename_emotions:
        file = open(i,'r',encoding='utf-8')
        emodict.append([line.strip() for line in file.readlines()])
        file.close()
    def splitword():  #分词获取情绪以及对应的时间地点
        nonlocal emodict
        emotion_list,time_list,address_list = [],[],[]
        for i in range(n):
            emotion_dict = {'anger':0,'disgust':0,'fear':0,'joy':0,'sadness':0}
            splitword = jieba.lcut(sentence[i])
            #print(splitword)
            for word in splitword:
                if word in emodict[0]:
                    emotion_dict['anger']+=1
                elif word in emodict[1]:
                    emotion_dict['disgust']+=1
                elif word in emodict[2]:
                    emotion_dict['fear']+=1
                elif word in emodict[3]:
                    emotion_dict['joy'] +=1
                elif word in emodict[4]:
                    emotion_dict['sadness']+=1
            if max(emotion_dict.values())==0:
                emotion = 'none'
            else:
                emotion = max(emotion_dict,key=emotion_dict.get)
            emotion_list.append(emotion)
            time_list.append(data[i][3])
            address_list.append(data[i][0])
        #print(address_list,end = '')
        return emotion_list,time_list,address_list
    return splitword

def ftime_list(time_list,n):
    """

    """
    time_list_new=[[]for i in range(n)]
    for i in range(n):
        time_list_new[i].append(time_list[i][:3])
        time_list_new[i].append(time_list[i][4:7])
        time_list_new[i].append(time_list[i][11:13])
    return time_list_new

def fplotime(emotion,time_mode,emotion_list,time_list):
    """
    生成指定情绪指定模式的情绪统计图
    :emotion:目标的情绪的字符串
    :time_mode:目标的时间图表模式
    :emotion_list:微博情绪列表
    :time_list:微博时间列表
    """
    week = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    week_dict = {}
    week_dict = week_dict.fromkeys(week,0)

    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_dict = {}
    month_dict = month_dict.fromkeys(month,0)

    hour = ['{:0>2d}'.format(i) for i in range(24)]
    hour_dict = {}
    hour_dict = hour_dict.fromkeys(hour,0)

    if time_mode == 'week':
        for tm in time_list:
            if emotion_list[time_list.index(tm)] == emotion:
                week_dict[tm[0]] += 1
        week_value = []
        for value in week_dict.values():
            week_value.append(value)
        plt.plot(week,week_value,'o-',color='r',label='week_{}'.format(emotion))
        plt.xlabel("week")#横坐标名字
        plt.ylabel("times")#纵坐标名字
        plt.legend(loc = "best")#图例
        for a,b in zip(week,week_value):
            plt.text(a,b+1,b,ha = 'center',va = 'bottom',fontsize=10)
        #print(week_dict)
    elif time_mode == 'month':
        for tm in time_list:
            if emotion_list[time_list.index(tm)] == emotion:
                month_dict[tm[1]] += 1
        month_value = []
        for value in month_dict.values():
            month_value.append(value)
        plt.plot(month,month_value,'o-',color='b',label='month_{}'.format(emotion))
        plt.xlabel("month")#横坐标名字
        plt.ylabel("times")#纵坐标名字
        plt.legend(loc = "best")#图例
        for a,b in zip(month,month_value):
            plt.text(a,b+1,b,ha = 'center',va = 'bottom',fontsize=10)
        #print(month_dict)    
    elif time_mode == 'hour':
        for tm in time_list:
            if emotion_list[time_list.index(tm)] == emotion:
                hour_dict[tm[2]] += 1
        hour_value = []
        for value in hour_dict.values():
            hour_value.append(value)
        plt.plot(hour,hour_value,'o-',color='y',label='hour_{}'.format(emotion))
        plt.xlabel("hour")#横坐标名字
        plt.ylabel("times")#纵坐标名字
        plt.legend(loc = "best")#图例
        for a,b in zip(hour,hour_value):
            plt.text(a,b+1,b,ha = 'center',va = 'bottom',fontsize=10)
        #print(hour_dict)
    else:
        print('Error!Please choose the right time mode.')
    plt.savefig('{}_{}.png'.format(time_mode,emotion),dpi=800)
    plt.show()

def emotion_admode(address_list,emotion_list,n):
    """
    画出位置分布图
    :address_list:微博地址列表
    :emotion_list:微博情绪列表
    :n:列表长度
    """
    x_list=[]
    y_list=[]
    add_emotion = []
    color_list = ['red','green','purple','yellow','blue']
    for i in range(n):
        zuobiao = address_list[i].split(',')
        x_list.append(float(zuobiao[0][1:]))
        y_list.append(float(zuobiao[1][:-1]))
        add_emotion.append(emotion_list[i])
    for i in range(5):
        x=[]
        y=[]
        for j in range(n):
            if EMO[i] == add_emotion[j]:
                x.append(x_list[j])
                y.append(y_list[j])
        plt.scatter(x,y, c = color_list[i])
        plt.title('The Space Mode of ' + EMO[i])
        plt.show()

def main():
    """
    main函数
    """
    txt=fread_document(filename_0_test) #读取txt文件
    m=len(txt)
    txt=fdelete_repetition_txt(txt) #删除重复项
    n=len(txt) #记录项数
    print("处理前数据有%d项.\n处理重复数据后有%d项." %(m,n))
    data=fcut_txt(txt,n) #简单切割内容、地址、时间
    n=len(data)#更新项数
    print(n)
    sentence = fdelete_url_data(data,n) #简单分词处理
    sentence = fclean_sentence(sentence,n) #正则表达式降噪
    #faddword(filename_emotions) #添加情绪词
    f=fdic_emotion(filename_emotions,data,sentence,n)
    emotion_list,time_list,address_list = f()
    time_list_new=ftime_list(time_list,n)
    '''
    for emotion in EMO:
        for timemode in TIMEMODE:
            fplotime(emotion,timemode,emotion_list,time_list_new)
    '''
    emotion_admode(address_list,emotion_list,n)

if __name__ == '__main__':
    main()