from functools import wraps
from playsound import playsound
from time import sleep

filename1 = r"C:\Users\LF\Desktop\music1.mp3"
filename2 = r"C:\Users\LF\Desktop\music2.mp3"
filename3 = r"C:\Users\LF\Desktop\music3.mp3"
filename4 = r"C:\Users\LF\Desktop\music4.mp3"

class Remind:
    """
    修饰器类
    """
    def __init__(self):
        pass
    
    def __remind(self,type_res):
        """
        内部方法
        用作实现修饰器中的提醒功能
        """
        if type_res == int:
            playsound(filename1)
        elif type_res == str:
            playsound(filename2)
        elif type_res in [list,dict,tuple]:
            playsound(filename3)
        else:
            playsound(filename4)

    def __call__(self,func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            res = func(*args,**kwargs)
            for i in range(len(res)):
                self.__remind(type(res[i]))
            return res
        return wrapper

@Remind()
def fun_test(*args,**kwargs):
    """
    用作测试
    返回输入的参数
    """
    sleep(5)
    return *args,*kwargs

def main():
    a = 1
    b = [1,2]
    c = {'a':1,'b':2}
    print(fun_test(b,a,c))

if __name__ == '__main__':
    main()