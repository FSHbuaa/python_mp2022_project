#-*- coding: gbk -*-

import networkx as nx
import pickle

filename_edges=r'C:\Users\LF\Desktop\twitch_gamers\large_twitch_edges.csv'
filename_features=r'C:\Users\LF\Desktop\twitch_gamers\large_twitch_features.csv'
filename_save=r'C:\Users\LF\Desktop\twitch_gamers\save.txt'

def init_node(filename_features):
    """
    返回字典，key 为节点的 ID，值为该节点对应的各属性值（可以同样设计为字典或列表）
    """
    print("----------正在导入数据----------")
    f=open(filename_features,encoding='UTF-8')
    title = f.readline().strip().split(',') #读取第一行
    txt_features=[]
    line=[1]
    while line:  # 直到读取完文件
        line = f.readline().strip()  # 读取一行文件，包括换行符
        txt_features.append(line)
    f.close()  # 关闭文件
    if txt_features[-1]=='':
        txt_features.pop()
    list_features=[]
    for i in txt_features:
        list_features.append(i.split(','))
    #print(list_features)
    print("----------数据导入完成----------")
    #print(title)
    dict_id={}       #用户属性字典
    for item in list_features:
        dict_index = {'views': "NULL", 'mature': "NULL", 'life_time': "NULL",
                'created_at': "NULL", 'updated_at': "NULL", 'dead_account': "NULL", 'language': "NULL", 'affiliate': "NULL"}
        for i in range(9):
            dict_index[title[i]] = item[i]
        dict_id[item[5]] = dict_index
    #print(len(dict_id))
    #print(dict_id)
    return dict_id

def get_features(G,id,features):
    """
    获取节点 node 的 指定属性。
    属性包括views，mature，life_time，created_at，updated_at，dead_account，language和affiliate
    """
    lis_features=['views','mature','life_time','created_at','updated_at','dead_account','language','affiliate']
    if features in lis_features:
        return G.nodes[id][features]
    else:
        return -1

def init_graph(filename_edges,dict_id):#（可以考虑用 networkx 中的 Graph 等。）
    """
    构建网络
    """
    print("----------正在导入边关系数据----------")
    f=open(filename_edges,encoding='UTF-8')
    title = f.readline().strip().split(',') #读取第一行
    txt_edges=[]
    line=[1]
    while line:  # 直到读取完文件
        line = f.readline().strip()  # 读取一行文件，包括换行符
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

def print_node(G,id):
    """
    显示节点全部信息（利用 format 或者 f 函数）
    """
    print("id为{0}的全部信息列表为{1}".format(id,G.nodes[id]))

dict_id=init_node(filename_features)
G=init_graph(filename_edges,dict_id)
save_graph(G,filename_save)
G=load_graph(filename_save)
#print(get_features(G,'5','views'))
#print_node(G,'5')