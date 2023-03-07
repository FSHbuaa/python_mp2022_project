from pathlib import Path

def get_lis(path):
    path_class = Path(path)
    path_generate = path_class.rglob('*')
    lis_path=[]
    for i in path_generate:
        path_str = str(i)
        name = path_str.split('/')[-1]
        if name[0] != '.' and 'jpg' in name:
            lis_path.append(i)
    return lis_path

path = r'C:\Users\LF\Desktop\originalPics'
print(get_lis(path))