from functools import wraps
import sys

path = r'C:\Users\LF\Desktop'

def saveprint(path):
    """
    带参数的修饰器
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            sys.stdout = open(path + '\\print.log', mode = 'w',encoding = 'utf-8')
            res = func(*args,**kwargs)
            return res
        return wrapper
    return decorator

@saveprint(path)
def fun_test():
    """
    测试用函数
    """
    for i in range(5):
        print(i)

def main():
    fun_test()

if __name__ == '__main__':
    main()