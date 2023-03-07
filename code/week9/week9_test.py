from pathlib import Path

path = r'C:\Users\LF\Desktop\originalPics'

P1 = Path(path)

path_generator = P1.rglob(r"*")

count = 0


for i in filter(lambda x : '.jpg' in str(x),path_generator):
    print(i)
    if count > 50:
        break
    count += 1