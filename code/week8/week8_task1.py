import os
from functools import wraps

path = r'C:\Users\LF\Desktop\week8_task1'

def check_path(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print("path is "+args[0])
        if not os.path.exists(args[0]):
            print("There's no such path.New is created.")
            os.mkdir(path)
        else:
            print("Path exists.\n")
        return func(*args,**kwargs)
    return wrapper

@check_path
def save(path,name_txt,txt):
    filenme = path + '\\' + name_txt + '.txt'
    with open(filenme,"w") as f:
        f.write(txt)


def main():
    txt = 'python is my favourite'
    name_txt = 'save'
    save(path,name_txt,txt)
    
if __name__ == '__main__':
    main()