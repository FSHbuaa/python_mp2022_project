#-*- coding: gbk -*-
def init_node(filename_features):
    """
    �����ֵ䣬key Ϊ�ڵ�� ID��ֵΪ�ýڵ��Ӧ�ĸ�����ֵ������ͬ�����Ϊ�ֵ���б�
    """
    print("----------���ڵ���ڵ���������----------")
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
    ��ȡ�ڵ�node��ָ�����ԡ�
    ���԰���views��mature��life_time��created_at��updated_at��dead_account��language��affiliate
    """
    lis_features=['views','mature','life_time','created_at','updated_at','dead_account','language','affiliate']
    if features in lis_features:
        return G.nodes[id][features]
    else:
        return -1

def print_node(G,id):
    """
    ��ʾ�ڵ�ȫ����Ϣ������ format��
    """
    print("idΪ{0}��ȫ����ϢΪ{1}".format(id,G.nodes[id]))
