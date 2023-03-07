import csv
from fileinput import filename
import jieba
import random
import math
import wordcloud

filename_0=r'C:\Users\LF\Desktop\弹幕数据\test_danmuku.csv'      #原始需读入文件
filename_1=r'C:\Users\LF\Desktop\弹幕数据\items.csv'        #需写入文件
filename_2=r'C:\Users\LF\Desktop\弹幕数据\stopwords_list.txt' #需读入停词表
filename_3=r'C:\Users\LF\Desktop\弹幕数据\myself.jpg'

data = []
text_all = ''
with open(filename_0,encoding='UTF-8') as csvfile:
    csv_reader = csv.reader(csvfile)   # 使用csv.reader读取csvfile中的文件
    header = next(csv_reader)          # 读取第一行每一列的标题
    for row in csv_reader:             # 将csv 文件中的数据保存到data中
        data.append(row[0])            # 选择弹幕列加入到data数组中
        text_all += row[0]             #连接所有弹幕字符串
##print(len(data))
##print(text)

#使用精确模式进行分词
count  = jieba.lcut(text_all)
##print(count)

'''
#定义空字典，对分词结果进行词频统计
word_count={}
for word in count:
    word_count[word] = word_count.get(word, 0) + 1  #若字典存在key则频数加一否则创建key并令值为1
'''

#添加停词表的新词频统计
word_count={}
word_lis=[]
stopwords = [line.strip() for line in open(filename_2,encoding='UTF-8').readlines()]
for word in count:
        if word not in stopwords and word != ' ':
            word_count[word] = word_count.get(word, 0) + 1
            word_lis.append(word)
new_text = ' '.join(word_lis)
##print(new_text)

#按词频对分词进行排序
items = list(word_count.items())                    #把字典转换为列表方便排序
items.sort(key=lambda x: x[1], reverse=True)
##print(items)


#对items根据词频进行特征词筛选，只保留次数大于等于5的高频词
n_items=len(items)
##print(n_items)
items_new=[[i for i in range(2)]for i in range(n_items)]
j=0
for i in range(n_items):
    if items[i][1] >= 5:
        items_new[j][0] = items[i][0]
        items_new[j][1] = items[i][1]
    j+=1

'''
#输出个csv看一看
with open(filename_1, 'w',encoding='UTF-8',newline='') as f:
    writer = csv.writer(f)
    for i in items_new:
        if i[0] != 0:
            writer.writerow(i)
'''

#写个关键词列表函数
def flis_key(words):
    lis_key=[]
    for item in items_new:
        if item[0] == 0:
            break
        elif item[0] in words:
            lis_key.append(1)
        else:
            lis_key.append(0)
    return lis_key

#获得10条有效弹幕，并输出他们的关键词列表
lis_danmu=[]                                           #一维列表，用来存储弹幕内容
lis_key_matrix=[]                                      #二维列表，用来存储10条弹幕的关键词0、1属性
for i in range(10):
    while True:
        number = random.randint(0,len(data)-1)         #获取随机弹幕的编号
        if len(data[number]) >= 15:                    #取字数大于15的有效弹幕
            break
    lis_danmu.append(data[number])
    lis_key_matrix.append(flis_key(data[number]))
    ##print(flis_key(data[number]))
##print(lis_key_matrix[0])

#输出抽取的10条弹幕
print("抽取的10条弹幕分别是：")
print("\n".join(i for i in lis_danmu))

#找到随机10条弹幕中1数量最多的最典型弹幕
lis_total_key=[0 for i in range(len(lis_danmu))]
count_1=0
for lis in lis_key_matrix:
    for i in lis:
        lis_total_key[count_1]+=i
    count_1+=1
##print(lis_total_key)
n_typical = lis_total_key.index(max(lis_total_key))
print("最典型的弹幕是\"%s\"" %(lis_danmu[n_typical]))


#写个计算欧式距离的函数
def fdis(lis_a,lis_b):
    '''
    需要两个lis的长度相同
    '''
    s=0
    for i in range(len(lis_a)):
        if lis_a[i] != lis_b[i]:
            s+=1
    return math.sqrt(s)
##print(fdis(lis_key_matrix[0],lis_key_matrix[1]))

#计算每个弹幕距离其他弹幕的距离
lis_dis_matrix=[[0 for i in range(10)]for i in range(10)]
for i in range(10):
    for j in range(10-i):
        lis_dis_matrix[i][j] = fdis(lis_key_matrix[i],lis_key_matrix[j])

#找到最大距离值
lis_col_dis_max = []
lis_col_num_max = []
for i in lis_dis_matrix:                                                       #先找到最大每行的最大值
    lis_col_dis_max.append(max(i))
    lis_col_num_max.append(i.index(max(i)))
dis_max_num = lis_col_dis_max.index(max(lis_col_dis_max))                              #找到全部的最大值
##print(lis_dis_matrix)
print("抽取的10条弹幕中距离最远的两条弹幕是:\n\"%s\"和\"%s\"\n它们之间的欧式距离为%.2f."%(lis_danmu[dis_max_num],lis_danmu[lis_col_num_max[dis_max_num]],max(lis_col_dis_max)))

#同理找到最小距离值
for i in lis_dis_matrix:                                        #排除完全相同的弹幕
    for j in range(len(i)):
        if int(i[j]) == 0:
            i[j]+=10
lis_col_dis_min = []
lis_col_num_min = []
for i in lis_dis_matrix:                                                       #先找到最大每行的最小值
    lis_col_dis_min.append(min(i))
    lis_col_num_min.append(i.index(min(i)))
dis_min_num = lis_col_dis_min.index(min(lis_col_dis_min))                              #找到全部的最小值
##print(lis_dis_matrix)
print("抽取的10条弹幕中距离最近的两条弹幕是:\n\"%s\"和\"%s\"\n它们之间的欧式距离为%.2f."%(lis_danmu[dis_min_num],lis_danmu[lis_col_num_min[dis_min_num]],min(lis_col_dis_min)))

#高频词可视化
w=wordcloud.WordCloud(width=1000,font_path="C:\\Windows\\Fonts\\simfang.ttf",height=700)
w.generate(new_text)
w.to_file("core words.png")