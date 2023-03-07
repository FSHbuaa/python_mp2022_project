import json
from multiprocessing import Process,Queue
import time
import random
import jieba

filename = r'C:\Users\LF\Desktop\sohu_data\sohu_data.json'
filename_test = r'C:\Users\LF\Desktop\sohu_data\sohu_data_test.json'

def load(path):
    with open(path,'r',encoding = 'utf-8') as fp:
        data = json.load(fp) #使用json模块读取文件
    content_lis=[]
    for dic in data:
        content_lis.append(dic['content'])
    return content_lis

def Map(content_lis,q):
    time.sleep(random.random())
    for i in content_lis:
        text_lis = jieba.lcut(i)
        for j in text_lis:
            q.put(j)
            print(j)
    print('end')

def Reduce(q):
    dic = {}
    while True:
        item = q.get()
        print(item)
        if item is None:
            print('end')
            break
        else:
            dic[item] = dic.get(item,0)+1
    dic_order=sorted(dic.items(),key=lambda x:x[1],reverse=True)  #字典降序排序
    with open('data.txt','w',encoding='utf-8') as file:
        for k,v in dic_order:
            file.write(k+':'+str(v)+'\n')  #将结果写入文件

if __name__=='__main__':
    content_lis = load(filename_test)
    num_lis = len(content_lis)
    q = Queue()
    q.put(None)
    process = []
    num_process = 2
    num_task = int(num_lis / num_process)
    for i in range(num_process):
        if i == num_process - 1:
            content_i_lis = content_lis[i*num_task:]
        else:
            content_i_lis = content_lis[i*num_task:(i+1)*num_task]
        content_i_lis = content_lis[0:2]
        p = Process(target = Map,args = (content_i_lis,q))
        process.append(p)
    for p in process:
        p.start()  #启动进程
    for p in process:
        pass
        #p.join()  #阻滞主进程
    time.sleep(10)
    print('main')
    Reduce(q)
    print('end')