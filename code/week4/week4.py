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

#��һ���֣��������������л�
#dict_id=gnn.init_node(filename_features)
#G=gng.init_graph(filename_edges,dict_id)
#gng.save_graph(G,filename_save)

#�ڶ����֣������л����������
G=gng.load_graph(filename_save)
#gnn.print_node(G,'5') #������һ��id����Ϣ
#print("�ܽ����Ϊ%d."%gns.get_node_number(G))
#print("�ܱ���Ϊ%d."%gns.get_edge_number(G))
#print("�����е�ƽ����Ϊ%d"%gns.cal_average_degree(G))

#�������֣�ͼ�Ŀ��ӻ�
#gvpg.plot_ego(G,str(random.randint(0,10)))
degree_dis = gns.cal_degree_distribution(G)
gvpg.plot_degree_distribution(degree_dis)
#gvpn.plot_degree_distribution(G,'views')