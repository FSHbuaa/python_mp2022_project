from pathlib import Path
import numpy as np
from PIL import Image

class FaceDataset:
    def __init__(self,image_path,start = 0,step = 1,max = 10):
        """
        :max:max的值不取
        """
        self.image_path = image_path
        self._start=start
        self._step=step
        self._max=max
        self._a=self._start
        self._list = self.load_dir(self.image_path)    # 调用静态方法获得文件目录列表
    
    @staticmethod
    def load_dir(image_path):
        P_image = Path(image_path)
        path_generator = P_image.rglob(r"*")                            #获得给定地址下的所有文件
        return list(filter(lambda x : '.jpg' in str(x),path_generator)) #返回后缀为'.jpg'的文件地址列表

    @staticmethod
    def load_image(a,lis):
        img = Image.open(lis[a])
        img = np.array(img)
        return img

    def __iter__(self):
        return self

    def __next__(self):
        if self._a < self._max:
            x = self.load_image(self._a,self._list)
            self._a += self._step
            return x
        else:
            raise StopIteration('达到max:{}'.format(self._max))

def main():
    path = r'C:\Users\LF\Desktop\originalPics'
    FD1 = FaceDataset(path)
    for i in FD1:
        print(i)
    print("-"*50)
    FD2 = FaceDataset(path)
    while True:
        try:
            print(next(FD2))
        except StopIteration as si:
            print(si.value)
            break

if __name__ == '__main__':
    main()