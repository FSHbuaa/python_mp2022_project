import json

filename = r'C:\Users\LF\Desktop\sohu_data\sohu_data.json'
filename_test = r'C:\Users\LF\Desktop\sohu_data\sohu_data_test.json'
filename_fin = r'C:\Users\LF\Desktop\sohu_data\sohu_data_fin.json'

def main():
    with open(filename,'r',encoding = 'utf-8') as fp:
        print(type(fp))
        data = json.load(fp) #使用json模块读取文件
    print(type(data))    #data的类型是列表
    print(type(data[0])) #data是一个字典列表，data[0]的类型是dict
    print(data[0]) #查看具体某个字典内容
    print(len(data)) #查看文件总长度
    print(len(data[0])) #单个字典长度
    
    #下面截取原json文件的一部分创建新的文件
    data_new=data[:1000]
    with open(filename_test,'w',encoding = 'utf-8') as fp:
        json.dump(data_new,fp,ensure_ascii=False)
    with open(filename_test,'r',encoding = 'utf-8') as fp:
        print(type(fp))
        data = json.load(fp) #使用json模块读取文件
    print(type(data))    #data的类型是列表
    print(type(data[0])) #data是一个字典列表，data[0]的类型是dict
    print(data[0]) #查看具体某个字典内容
    print(len(data)) #查看文件总长度
    print(len(data[0])) #单个字典长度

if __name__ == '__main__':
    main()