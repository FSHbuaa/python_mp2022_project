#-*- coding: gbk -*-
import seaborn as sns
import networkx as nx
import GraphStat.NetworkBuilder.stat as gns
import matplotlib.pyplot as plt

def plot_degree_distribution(G,features):
    """
    观察属性的分布形态
    """
    node=G.nodes()
    lis=['views', 'mature', 'life_time', 'created_at', 'updated_at', 'numeric_id', 'dead_account', 'language', 'affiliate']
    if features in lis:
        lis1=[]
        lis2=[0,50000,100000,150000]
        dic=gns.cal_distribution(G,features)
        for i in dic:
            lis1.append(dic[i])
        sns.set(palette='muted',color_codes=True)
        sns.distplot(lis1,lis2,hist=False,color='g',kde_kws={'shade':True})
        plt.show()
        