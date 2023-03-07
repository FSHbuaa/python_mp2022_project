#-*- coding: gbk -*-
import networkx as nx
import pickle

def init_graph(filename_edges,dict_id):#�����Կ�����networkx�е� Graph �ȡ���
    """
    ��������
    """
    print("----------���ڵ���߹�ϵ����----------")
    f=open(filename_edges,encoding='UTF-8')
    title = f.readline().strip().split(',')     #��ȡ��һ��
    txt_edges=[]
    line=[1]
    while line:       #ֱ����ȡ���ļ�
        line = f.readline().strip()  #��ȡһ���ļ����������з�
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