#-*- coding: gbk -*-
import networkx as nx

def get_node_number(G):
    """
    计算节点数
    """
    number=nx.number_of_nodes(G)
    return number

def get_edge_number(G):
    """
    计算边数
    """
    number=nx.number_of_edges(G)
    return number

def cal_average_degree(G):
    """
    计算网络中的平均度
    """
    node=G.nodes()
    sum=0
    for i in node:
        sum+=G.degree(i)
    return sum/len(node)

def cal_degree_distribution(G):
    """
    计算网络的度分布
    """
    degree_dis=nx.degree_histogram(G)#统计从0到最大度的频次
    lis = [z / float(sum(degree_dis)) for z in degree_dis]#生成密度列表
    return lis

def cal_distribution(G,features):
    """
    计算 features 属性的分布
    """
    view_dic={}
    for id in G.nodes():#生成字典
        view_dic[G.nodes[id][features]]=view_dic.get(G.nodes[id][features],0)+1
    sum=0
    for key in view_dic.keys():
        sum+=view_dic[key]
    for key in view_dic.keys():
        view_dic[key]=view_dic[key]/sum
    return view_dic