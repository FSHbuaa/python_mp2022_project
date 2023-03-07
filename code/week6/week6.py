import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFilter
import os
import glob

class Filter:
    """
    基类Filter
    """
    def __init__(self,image,parameters):
        """
        image:待处理的图片实例 
        parameters:滤波器参数
        """
        self.image = image
        self.parameters = parameters

    def filter(self):
        """
        在基类中不进行实现
        实现细节交给子类
        """
        pass

class Edge(Filter):
    """
    边缘提取子类Edge
    """
    def __init__(self,image,parameters):
        super(Edge,self).__init__(image,parameters)

    def filter(self,img):
        img = img.filter(ImageFilter.FIND_EDGES)
        return img

class Blur(Filter):
    """
    模糊子类Blur
    """
    def __init__(self,image,parameters):
        super(Blur,self).__init__(image,parameters)
        
    def filter(self,img):
        img = img.filter(ImageFilter.BLUR)
        return img

class Sharpen(Filter):
    """
    锐化子类Sharpen
    """
    def __init__(self,image,parameters):
        super(Sharpen,self).__init__(image,parameters)
        
    def filter(self,img):
        img = img.filter(ImageFilter.SHARPEN)
        return img

class Resize(Filter):
    """
    大小调整子类Resize
    """
    def __init__(self,image,parameters):
        super(Resize,self).__init__(image,parameters)
        
    def filter(self,img):
        img = img.resize((self.parameters[0],self.parameters[1]))
        return img

class ImageShop:
    """
    图片处理类
    """
    def __init__(self,formation,path,Image_list,Image_process):
        """
        formation:图片格式
        path:图片目录
        Image_list:储存图片实例（初始传参传入空列表）
        Image_process: 储存处理过的图片（初始传参传入空列表）
        """
        self.formation = formation
        self.path= path
        self.Image_list = Image_list
        self.Image_process = Image_process

    def __load_images(self):
        """
        内部方法
        加载指定目录下所有格式为formation的图片
        """
        self.Image_list = glob.glob(os.path.join(self.path,'*'+self.formation))

    def __batch_ps(self,Filter):
        """
        处理图片的内部方法
        """
        for i in range(len(self.Image_process)):
            img = Filter.filter(self.Image_process[i])  #调用对应Filter类的filter方法
            self.Image_process[i] = img

    def batch_ps(self,*args):
        """
        批量处理图片的对外公开方法
        args为不定长的tuple形如(operation,parameters)
        """
        ImageShop.__load_images(self)                   #加载图片路径
        for i in self.Image_list:
            self.Image_process.append(Image.open(i))
        for image in self.Image_process:
            for i in range(len(args)):
                if args[i][0] == 'Edge':
                    edge = Edge(image,args[i][1])
                    ImageShop.__batch_ps(self,edge)
                elif args[i][0] == 'Sharpen':
                    sharpen = Sharpen(image,args[i][1])
                    ImageShop.__batch_ps(self,sharpen)
                elif args[i][0] == 'Blur':
                    blur = Blur(image,args[i][1])
                    ImageShop.__batch_ps(self,blur)
                elif args[i][0] == 'Resize':
                    resize = Resize(image,args[i][1])
                    ImageShop.__batch_ps(self,resize)

    def display(self,row = 3,column= 3,maximum = 27):
        """
        利用subplot函数批量显示处理后图片
        row:每行图片数
        column:每列图片数
        maximum:处理图片最大数量
        在默认情况最多输出3页
        """
        if len(self.Image_process) > maximum:
            self.Image_process = self.Image_process[:maximum]
        plt.ion()      #为了使循环能够正常进行
        for page in range(0,len(self.Image_process),row * column):     #控制每一页生产的图片数量
            for i in range(row * column):                      #控制每张子图展示图片数量
                if page + i <len(self.Image_process):
                    img = self.Image_process[page + i]
                    plt.subplot(row,column,i + 1)
                    plt.imshow(img)
                else:
                    continue
            plt.show()
            plt.pause(10)    #等待10秒后关闭当前页
            plt.close('all')
   
    def save(self,filepath):
        """
        保存图片到指定路径
        """
        for num in range(len(self.Image_process)):
            img = self.Image_process[num]
            img.save(filepath+'\{}'.format(num) + self.formation)
            
class TestImageShop:
    """
    测试类
    """
    def __init__(self,formation,path,Image_list,Image_process):
        self.Test = ImageShop(formation,path,Image_list,Image_process)

    def batch(self,*args):
        self.Test.batch_ps(*args)

    def save(self,filepath):
        self.Test.save(filepath)

    def display(self):
        self.Test.display()

def main():
    """
    main函数
    """
    #给定的参数
    parameters = [640,480]
    path = r'C:\Users\LF\Desktop\animals'   #图片集路径
    formation = '.png'
    Image_list,Image_process = [],[]
    operation = ['Edge','Sharpen','Blur','Resize']
    filepath = r'C:\Users\LF\Desktop\week6'
    #使用测试类测试
    test = TestImageShop(formation,path,Image_list,Image_process)
    test.batch((operation[1],0),(operation[2],0),(operation[3],parameters))
    #test.batch((operation[3],parameters))
    test.save(filepath)
    test.display()

if __name__ == '__main__':
    main()