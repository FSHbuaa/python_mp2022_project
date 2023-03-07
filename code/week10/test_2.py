import collections
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt

filename = r'C:\Users\LF\Desktop\out.txt'

with open(filename, encoding='UTF-8') as f:
	data = f.read()
wordList_jieba = jieba.lcut(data)
deal_a=[]
for i in wordList_jieba:
    if len(i)>1:
        deal_a.append(i)
x = dict(collections.Counter(deal_a))


font = r'C:\Windows\Fonts\STKAITI.ttf'
stopwords_filepath =  r'C:\Users\LF\Desktop\stopwords_list.txt'
stopwords_file=[]
with open(stopwords_filepath, encoding='UTF-8') as f:
    stopwords_file = f.readlines()
stopwords = [word.strip() for word in stopwords_file]

# 词云分析
wc = WordCloud(font,max_words=50,stopwords=stopwords,background_color="white",width = 1500,height= 960,margin= 10)
#fit_words(参数)是WordCloud的子函数，用于根据词频绘制词云，这里的参数一般是字典类型变量
t = wc.fit_words(x)
t.to_image().save('词云.png')
# 词云展示
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()