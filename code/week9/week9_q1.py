import numpy as np

def random_walk(mu,X_0,sigma_square,N):
    w = np.random.normal(0,sigma_square,N)
    X_t = X_0
    t = 1
    X_t = mu + X_t + w[t] 
    while(t < N):
        yield X_t
        X_t = mu + X_t + w[t] 
        t += 1
    return 'done'

def main():
    rw1 = random_walk(0,0,1,10)
    for f in rw1:
        pass
        print(f)
    print("-"*50)
    rw2 = random_walk(1,0,1,20)
    while True:
        try:
            print(next(rw2))
        except StopIteration as si:
            print(si.value)
            break
    rw3 = random_walk(0,0,1,10)
    rw4 = random_walk(0,0,1,10)
    z=zip(rw3,rw4)
    print(*z)

if __name__ == '__main__':
    main()