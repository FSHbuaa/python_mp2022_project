#-*- coding: gbk -*-

import networkx as nx
import pickle

filename_edges=r'C:\Users\LF\Desktop\twitch_gamers\large_twitch_edges.csv'
filename_features=r'C:\Users\LF\Desktop\twitch_gamers\large_twitch_features.csv'
filename_save=r'C:\Users\LF\Desktop\twitch_gamers\save.txt'

def init_node(filename_features):
    """
    �����ֵ䣬key Ϊ�ڵ�� ID��ֵΪ�ýڵ��Ӧ�ĸ�����ֵ������ͬ�����Ϊ�ֵ���б�
    """
    print("----------���ڵ�������----------")
    f=open(filename_features,encoding='UTF-8')
    title = f.readline().strip().split(',') #��ȡ��һ��
    txt_features=[]
    line=[1]
    while line:  # ֱ����ȡ���ļ�
        line = f.readline().strip()  # ��ȡһ���ļ����������з�
        txt_features.append(line)
    f.close()  # �ر��ļ�
    if txt_features[-1]=='':
        txt_features.pop()
    list_features=[]
    for i in txt_features:
        list_features.append(i.split(','))
    #print(list_features)
    print("----------���ݵ������----------")
    #print(title)
    dict_id={}       #�û������ֵ�
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
    ��ȡ�ڵ� node �� ָ�����ԡ�
    ���԰���views��mature��life_time��created_at��updated_at��dead_account��language��affiliate
    """
    lis_features=['views','mature','life_time','created_at','updated_at','dead_account','language','affiliate']
    if features in lis_features:
        return G.nodes[id][features]
    else:
        return -1

def init_graph(filename_edges,dict_id):#�����Կ����� networkx �е� Graph �ȡ���
    """
    ��������
    """
    print("----------���ڵ���߹�ϵ����----------")
    f=open(filename_edges,encoding='UTF-8')
    title = f.readline().strip().split(',') #��ȡ��һ��
    txt_edges=[]
    line=[1]
    while line:  # ֱ����ȡ���ļ�
        line = f.readline().strip()  # ��ȡһ���ļ����������з�
        txt_edges.append(line)
    f.close()  # �ر��ļ�
    if txt_edges[-1]=='':
        txt_edges.pop()
    list_edges=[]
    for i in txt_edges:
        list_edges.append(i.split(','))
    #print(list_edges)
    print("----------�߹�ϵ���ݵ������----------")
    G = nx.Graph()#����һ���հ�ͼ
    for id in dict_id:
        for key in dict_id[id]:
            G.add_node(id) #�����
            G.nodes[id][key]=dict_id[id][key] #�������
    G.add_edges_from(list_edges) #���ӽڵ�
    return G

def save_graph(G,filename_save):     
    """
    ���л�ͼ��Ϣ
    ͼ����Ϣ��ʱ�����ַ�����ʽ�洢
    """
    f=open(filename_save,"wb")
    pickle.dump(G,f)
    f.close()


def load_graph(filename_save): 
    """
    ������������ڴ�
    """
    f=open(filename_save,"rb")
    result =pickle.load(f)
    f.close()
    return result

def print_node(G,id):
    """
    ��ʾ�ڵ�ȫ����Ϣ������ format ���� f ������
    """
    print("idΪ{0}��ȫ����Ϣ�б�Ϊ{1}".format(id,G.nodes[id]))

dict_id=init_node(filename_features)
G=init_graph(filename_edges,dict_id)
save_graph(G,filename_save)
G=load_graph(filename_save)
#print(get_features(G,'5','views'))
#print_node(G,'5')