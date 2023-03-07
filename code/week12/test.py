import random
class Apple:
    color = 'red'
    def __init__(self,size):
        #super().__init__()
        self.size = size

    def plant(self):
        pass

    def __str__(self):
        return 'apple'+ str(random.randint(1,5))
    
    def __call__(self):
        print("I'm called")
    
    def __add__(self1,self2):
        return Apple(self1.size + self2.size)

a1 = Apple(10)
a2 = Apple(5)
a3 = a1 + a2
