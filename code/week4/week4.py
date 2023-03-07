#-*- coding: gbk -*-
import GraphStat.NetworkBuilder.graph as gng
import GraphStat.NetworkBuilder.node as gnn
import GraphStat.NetworkBuilder.stat as gns
import GraphStat.Visualization.plotgraph as gvpg
import GraphStat.Visualization.plotnodes as gvpn
import random

filename_edges=r'C:\Users\LF\Desktop\twitch_gamers\large_twitch_edges.csv'
filename_features=r'C:\Users\LF\Desktop\twitch_gamers\large_twitch_features.csv'
filename_save=r'C:\Users\LF\Desktop\twitch_gamers\save.txt'

#第一部分：输入数据与序列化
#dict_id=gnn.init_node(filename_features)
#G=gng.init_graph(filename_edges,dict_id)
#gng.save_graph(G,filename_save)

#第二部分：反序列化与属性输出
G=gng.load_graph(filename_save)
#gnn.print_node(G,'5') #随便输出一个id的信息
#print("总结点数为%d."%gns.get_node_number(G))
#print("总边数为%d."%gns.get_edge_number(G))
#print("网络中的平均度为%d"%gns.cal_average_degree(G))

#第三部分：图的可视化
#gvpg.plot_ego(G,str(random.randint(0,10)))
degree_dis = gns.cal_degree_distribution(G)
gvpg.plot_degree_distribution(degree_dis)
#gvpn.plot_degree_distribution(G,'views')