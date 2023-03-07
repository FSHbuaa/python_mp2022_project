#-*- coding: gbk -*-
import networkx as nx
import GraphStat.NetworkBuilder.stat as gns
import matplotlib.pyplot as plt

def plot_ego(G,node):
    """
    ���ƽڵ�ľֲ�����
    """
    Q=nx.Graph()
    Q.add_node(node)
    lis=G.nodes()
    for i in lis:
        if G.has_edge(node,i):
            Q.add_node(i)
            Q.add_edge(i,node)
    nx.draw(Q,with_labels=True)
    plt.show()


def plot_degree_distribution(degree_dis): #���۲�ȷֲ�����̬��
    """
    �ȵķֲ�ͼ
    ���ڽڵ�ֲ����ڷ�ɢ�������������Ϊ0~200�ķֲ�
    """
    x=[i for i in range(150)]
    y=degree_dis[0:150]
    plt.plot(x,y,color="violet",linewidth=2.5)
    plt.title("degree distribution")
    plt.show()