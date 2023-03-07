import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

path = r'C:\Users\LF\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_20130301-20170228'

class DataNotNumError(ValueError):
    def __init__(self,region,year,month,day,hour,pollutant):
        self.region = region
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.pollutant = pollutant
        self.message = "{} {}-{}-{}-{} {} is not a valid number.".format(region,year,month,day,hour,pollutant)

class Data_process:
    def __init__(self,path):
        self.path=path
        self.filename_list = glob.glob(os.path.join(self.path,'*'+'.csv'))  #获得目标路径下的所有.csv文件
        #print(self.filename_list)
        self.station_list=[]
        for i in range(len(self.filename_list)):
            self.station_list.append(self.filename_list[i].split('_')[6])
        #print(self.station_list)

    def examine(self):
        """
        应在load前使用以确保数据形式正确
        """
        for i in self.filename_list:
            data = pd.read_csv(i,header = 0)
            x,y=map(list,np.where(data.isnull()))          #获得异常数据位置
            if len(x) > 0:
                for j in range(len(x)):
                    try:
                        pollutant = data.columns.values[y[j]]
                        year = data['year'][x[j]]
                        region = data['station'][x[j]]
                        month = data['month'][x[j]]
                        day = data['day'][x[j]]
                        hour = data['hour'][x[j]]
                        raise DataNotNumError(region, year, month, day, hour,pollutant)
                    except DataNotNumError as error:
                        print(error.message)
                    break
                data.fillna(method='pad', inplace=True)    #将数据按前一行补齐
                print('异常数据处理后异常状态为：（False即为无异常）')
                print(np.any(data.isnull()))
            break

    def load_data_csv(self,filename):
        """
        读取单个路径下的.csv文件并做初始化
        """
        dic_dtype={'No':int,'year':int,'month':int,'day':int,
        'hour':int,'PM2.5':float,'PM10':float,'SO2':float,
        'NO2':float,'CO':float,'O3':float,'TEMP':float,
        'PRES':float,'DEWP':float,'RAIN':float,'wd':str,
        'WSPM':float,'station':str}
        df = pd.read_csv(filename,header = 0,dtype=dic_dtype)
        periods = pd.PeriodIndex(year=df["year"],month=df["month"],
                                 day=df["day"],hour=df["hour"],freq="H")  #时间序列化
        df1 = df.set_index(periods)
        del_lis = ['No',"year","month","day","hour"]                      #删除无用列
        for i in del_lis:
            del df1[i]
        #print(df1)
        return df1


    def time_analyze(self,station,type,mod = 'M'):
        """
        station为需要分析的区名
        type为需要分析的数据名
        mod为时间分析的模式 默认为以月为单位
        输出对应模式对应排放量的数据分析
        返回pandas数组用以可视化
        """
        for i in range(len(self.station_list)):
            if self.station_list[i] == station:
                self.filename_time_analyze = self.filename_list[i]
        #print(self.filename_time_analyze)
        df = self.load_data_csv(self.filename_time_analyze)
        #print(df)
        df = df[type].resample(mod).mean()
        #print(df,df.index)
        for i in range(len(df)):
            print("{}的平均{}排放量为{:.1f}".format(df.index[i],type,df[i]))
        return df

    def space_analyze(self,type):
        """
        type为需要分析的数据名
        输出对应
        返回pandas数组用以可视化
        """
        df_space = pd.DataFrame()
        df_space['station'] = self.station_list
        data_list=[]
        for i in range(len(self.station_list)):
            df = self.load_data_csv(self.filename_list[i])
            data_list.append(df[type].mean())
        df_space[type] = data_list
        df_space = df_space.set_index('station')
        #print(df_space.index)
        for i in range(len(df_space)):
            print("{}近年的平均{}排放量为{:.1f}".format(df_space.index[i],type,df_space[type][i]))
        return df_space

class Data_view:
    def  __init__(self,data_time=[],data_space=[]):
        """
        将需要的时间与空间数据做初始化
        """
        self.data_time = data_time
        self.data_space = data_space
    
    def time_view(self):
        """
        画出对应的时间分布图
        """
        self.data_time.plot(subplots=True, figsize=(10,12))
        plt.show()

    def space_view(self):
        """
        画出对应的空间分布图
        """
        self.data_space.plot(kind = 'bar')
        plt.xticks(rotation = 360)
        plt.show()
        self.data_space.plot(kind = 'pie',subplots=True,autopct='%.2f%%')
        plt.show()

def main():
    Dp = Data_process(path)
    Dp.examine()
    dt = Dp.time_analyze(station = 'Aotizhongxin',type = 'SO2')
    ds = Dp.space_analyze(type = 'SO2')
    Dv=Data_view(data_time=dt,data_space=ds)
    Dv.time_view()
    Dv.space_view()
    

if __name__ == '__main__':
    main()