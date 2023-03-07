import sys
import line_profiler
import memory_profiler
import tqdm
import pysnooper

import jieba
import re
import matplotlib.pyplot as plt
import random

class Tokenizer:
    def __init__(self,chars,coding='c',PAD=0):
        """
        输入将要需要操作的文本，完成词典的构建
        coding='w'按词构建
        coding='c'按字构建（默认）
        PAD默认为0
        将字典赋值给dic_chars
        """
        self.chars=chars
        self.coding=coding
        self.PAD=PAD
        dic={}
        dic['[PAD]'] = 0
        code_number = 1
        if coding == 'c':
            self.len_all = len(chars)
            for char in tqdm.tqdm(chars):
                if char not in dic:
                    dic[char] = code_number
                    code_number += 1
        elif coding == 'w':
            lis_words=jieba.lcut(chars)
            self.len_all = len(lis_words)
            for word in lis_words:
                if word not in dic:
                    dic[word] = code_number
                    code_number += 1
        self.dic_chars=dic

    def tokenize(self, sentence) -> list:
        """
        输入句子sentence
        返回list_of_chars
        """
        list_of_chars=[]
        if self.coding == 'c':
            for char in sentence:
                list_of_chars.append(char)
        if self.coding == 'w':
            list_of_chars = jieba.lcut(sentence)
        return list_of_chars

    def encode(self, list_of_chars):
        """
        输入字符(字或者词）的字符列表，返回转换后的数字列表 (tokens)。
        """
        tokens = []
        for char in list_of_chars:
            tokens.append(self.dic_chars[char])
        return tokens

    def trim(self, tokens, seq_len):
        """
        输入数字列表tokens，整理数字列表的长度。不足seq_len的部分用PAD补足，超过的部分截断。
        """
        while len(tokens) < seq_len:
            tokens.append(0)
        if len(tokens) > seq_len:
            tokens = tokens[:seq_len]
        return tokens
    
    def decode(self, tokens):
        """
        将数字列表翻译回句子
        """
        for i in tokens:
            for k,v in self.dic_chars.items():
                if i == v:
                    print(k,end = '')
        print()
    
    def encode_all(self,seq_len) -> list:
        """
        返回所有文本(chars)的长度为seq_len的tokens
        """
        list_of_chars = self.tokenize(self.chars)
        tokens = self.encode(list_of_chars)
        lis_tokens = []
        num = len(tokens)
        for i in range(int(num / seq_len)):
           lis_tokens.append(tokens[seq_len * i:seq_len * i + seq_len])
        lis_tokens.append(self.trim(tokens[seq_len * int(num / seq_len):],seq_len))
        return lis_tokens

filename = r'C:\Users\LF\Desktop\final_none_duplicate.txt\test.txt'
filename_0_test = r'C:\Users\LF\Desktop\final_none_duplicate.txt\final_none_duplicate_test.txt'
filename_0 = r'C:\Users\LF\Desktop\final_none_duplicate.txt\final_none_duplicate.txt'

lp = line_profiler.LineProfiler()
mp = memory_profiler.profile()


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
        sentence[i] = re.sub(r"\[\S+\]", "", sentence[i])      # 去除表情符号
        sentence[i] = re.sub(r"#\S+#", "", sentence[i])      # 保留话题内容
    return sentence

@lp
def main():
    """
    main函数
    """
    txt=fread_document(filename_0_test) #读取txt文件
    m=len(txt)
    #txt=fdelete_repetition_txt(txt) #删除重复项
    n=len(txt) #记录项数
    #print("处理前数据有%d项.\n处理重复数据后有%d项." %(m,n))
    data=fcut_txt(txt,n) #简单切割内容、地址、时间
    n=len(data)#更新项数
    #print(n)
    sentence = fdelete_url_data(data,n) #简单分词处理
    sentence = fclean_sentence(sentence,n) #正则表达式降噪
    #print(sentence)
    chars = ''.join(sentence)
    #print(chars)
    #T_c = Tokenizer(chars,'c')
    #print("文本总长度为%d"%T_c.len_all)
    #print('按字编码的编码规模为%d'%len(T_c.dic_chars))
    #T_w = Tokenizer(chars,'w')
    #print("文本总词数为%d"%T_w.len_all)
    #print('按词编码的编码规模为%d'%len(T_w.dic_chars))
    T_c = Tokenizer(chars,'c')
    lis_token=[]
    seq_len = 34
    for i in range(10):
        number = random.randint(0,len(sentence)-1)
        lis_of_chars = T_c.tokenize(sentence[number])
        tokens = T_c.encode(lis_of_chars)
        tokens = T_c.trim(tokens,seq_len)
        lis_token.append(tokens)
    print("10条文本Trim后的token为：")
    for i in lis_token:
        print(i)
    print('------------------------------')
    print("10条文本解码后为：")
    for i in lis_token:
        T_c.decode(i)
    """
    list_of_chars = T.tokenize(sentence[10000])
    print(list_of_chars)
    tokens = T.encode(list_of_chars)
    print(tokens)
    if T.coding == 'c':
        seq_len = round(len(chars)/len(sentence))
    elif T.coding == 'w':
        seq_len = round(len(jieba.lcut(chars))/len(sentence))
    
    print('seq_len = %d'%seq_len)
    tokens = T.trim(tokens,seq_len)
    print(tokens)
    T.decode(tokens)
    print(T.encode_all(seq_len))
    """
    """
    lis_len=[]
    for i in sentence:
        lis_len.append(len(i))
    max_len=max(lis_len)
    dis_len=[0 for i in range(max_len+1)]
    for i in lis_len:
        dis_len[i] += 1
    n_txt = 0
    for i in dis_len:
        n_txt += i
    print(max_len)
    print(dis_len)
    x=[i for i in range(max_len+1)]
    y=dis_len
    plt.plot(x,y,color="purple",linewidth=2.5)
    plt.title("length distribution")
    plt.show()
    x=[i for i in range(50)]
    y=dis_len[:50]
    plt.plot(x,y,color="blue",linewidth=2.5)
    plt.title("length distribution")
    plt.show()
    count = 0
    lis_i = 0
    while(count < n_txt * 0.75):
        count += dis_len[lis_i]
        lis_i += 1
    print(lis_i-1)
    """
 



if __name__ == '__main__':
    main()
    lp.print_stats()

"""
with open(filename,'r',encoding='utf-8') as f:
    chars = f.read()
with open(filename,'r',encoding='utf-8') as f:
    string = f.readlines()
print(string[3])
T = Tokenizer(chars,'c')
list_of_chars = T.tokenize(string[3])
print(list_of_chars)
tokens = T.encode(list_of_chars)
print(tokens)
seq_len = 10
print('seq_len = %d'%seq_len)
tokens = T.trim(tokens,seq_len)
print(tokens)
T.decode(tokens)
print(T.encode_all(seq_len))
"""