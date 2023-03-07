import json
from multiprocessing import Process
from multiprocessing import Manager
import time
import jieba

filename = r'C:\Users\LF\Desktop\sohu_data\sohu_data.json'
filename_test = r'C:\Users\LF\Desktop\sohu_data\sohu_data_test.json'
filename_fin = r'C:\Users\LF\Desktop\sohu_data\sohu_data_fin.json'
filename_result = r'C:\Users\LF\Desktop\result_ori.txt'

def load(path):
    with open(path,'r',encoding = 'utf-8') as fp:
        data = json.load(fp) #使用json模块读取文件
    content_lis=[]
    for dic in data:
        content_lis.append(dic['content'])
    return content_lis

def Map(content_lis,Lis):
    for i in content_lis:
        text_lis = jieba.lcut(i)
        for j in text_lis:
            Lis.append(j)

def Reduce(Lis):
    dic = {}
    for i in Lis:
        dic[i] = dic.get(i,0)+1
    dic_order=sorted(dic.items(),key=lambda x:x[1],reverse=True)
    with open(filename_result,'w',encoding='utf-8') as file:
        for k,v in dic_order:
            file.write(str(k)+':'+str(v)+'\n')

if __name__=='__main__':
    content_lis = load(filename_test)
    num_lis = len(content_lis)
    m = Manager()
    Lis = m.list()
    process = []
    num_process = 100       #可给定任意的进程数
    num_task = int(num_lis / num_process)
    for i in range(num_process):
        if i == num_process - 1:
            content_i_lis = content_lis[i*num_task:]
        else:
            content_i_lis = content_lis[i*num_task:(i+1)*num_task]
        p = Process(target = Map,args = (content_i_lis,Lis))
        process.append(p)
    start_time = time.time() #进程启动前记录启动时间
    for p in process:
        p.start()  #启动进程
    for p in process:
        p.join()  #阻滞主进程
    Mapped_time = time.time()
    Map_cost_time = Mapped_time - start_time
    print('Map进程结束')
    #Reduce(Lis)
    #Reduced_time = time.time()
    #Reduce_cost = Reduced_time - Mapped_time
    #print('Reduce进程结束')
    print('-'*25)
    print(f'{num_process}个进程时，Map进程耗时{Map_cost_time:.2f}秒')
    #print(f'Reduce进程耗时{Reduce_cost:.2f}秒')