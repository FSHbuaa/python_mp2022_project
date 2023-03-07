#-*- coding: gbk -*-
import networkx as nx

def get_node_number(G):
    """
    ����ڵ���
    """
    number=nx.number_of_nodes(G)
    return number

def get_edge_number(G):
    """
    �������
    """
    number=nx.number_of_edges(G)
    return number

def cal_average_degree(G):
    """
    ���������е�ƽ����
    """
    node=G.nodes()
    sum=0
    for i in node:
        sum+=G.degree(i)
    return sum/len(node)

def cal_degree_distribution(G):
    """
    ��������Ķȷֲ�
    """
    degree_dis=nx.degree_histogram(G)#ͳ�ƴ�0�����ȵ�Ƶ��
    lis = [z / float(sum(degree_dis)) for z in degree_dis]#�����ܶ��б�
    return lis

def cal_distribution(G,features):
    """
    ���� features ���Եķֲ�
    """
    view_dic={}
    for id in G.nodes():#�����ֵ�
        view_dic[G.nodes[id][features]]=view_dic.get(G.nodes[id][features],0)+1
    sum=0
    for key in view_dic.keys():
        sum+=view_dic[key]
    for key in view_dic.keys():
        view_dic[key]=view_dic[key]/sum
    return view_dic