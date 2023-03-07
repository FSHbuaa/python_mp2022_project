#-*- coding: gbk -*-
import networkx as nx
import pickle

def init_graph(filename_edges,dict_id):#（可以考虑用networkx中的 Graph 等。）
    """
    构建网络
    """
    print("----------正在导入边关系数据----------")
    f=open(filename_edges,encoding='UTF-8')
    title = f.readline().strip().split(',')     #读取第一行
    txt_edges=[]
    line=[1]
    while line:       #直到读取完文件
        line = f.readline().strip()  #读取一行文件，包括换行符
        txt_edges.append(line)
    f.close()  # 关闭文件
    if txt_edges[-1]=='':
        txt_edges.pop()
    list_edges=[]
    for i in txt_edges:
        list_edges.append(i.split(','))
    #print(list_edges)
    print("----------边关系数据导入完成----------")
    G = nx.Graph()#生成一个空白图
    for id in dict_id:
        for key in dict_id[id]:
            G.add_node(id) #插入点
            G.nodes[id][key]=dict_id[id][key] #添加属性
    G.add_edges_from(list_edges) #连接节点
    return G

def save_graph(G,filename_save):     
    """
    序列化图信息
    图的信息暂时均以字符串形式存储
    """
    f=open(filename_save,"wb")
    pickle.dump(G,f)
    f.close()

def load_graph(filename_save): 
    """
    将网络加载至内存
    """
    f=open(filename_save,"rb")
    result =pickle.load(f)
    f.close()
    return result