#-*- coding: gbk -*-
def init_node(filename_features):
    """
    返回字典，key 为节点的 ID，值为该节点对应的各属性值（可以同样设计为字典或列表）
    """
    print("----------正在导入节点属性数据----------")
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
    获取节点node的指定属性。
    属性包括views，mature，life_time，created_at，updated_at，dead_account，language和affiliate
    """
    lis_features=['views','mature','life_time','created_at','updated_at','dead_account','language','affiliate']
    if features in lis_features:
        return G.nodes[id][features]
    else:
        return -1

def print_node(G,id):
    """
    显示节点全部信息（利用 format）
    """
    print("id为{0}的全部信息为{1}".format(id,G.nodes[id]))
