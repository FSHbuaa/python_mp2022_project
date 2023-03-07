import socket
import time
from threading import Thread

running = False

class Chatter:
    def send(c):
        time.sleep(0.5)
        while True:
            data = input('')
            c.send(data.encode("utf-8"))
            #file.write(data+'\n')
            #file.close()

            if data == "quit":
                running = False
                break

    def recv(c,t2):
        username = input("输入用户名:")
        #file = open(f'{username}.txt','a')
        #file.write("输入用户名:"+username+'\n')

        c.send(username.encode("utf-8"))
        t2.start()
        while running:
            try:
                data = c.recv(1024).decode("utf-8")
                if not data:
                    break
                print(data)
                #file.write(data+'\n')
                #file.close()
            except:
                break

if __name__ == "__main__":
    ip = "127.0.0.1"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 导入 socket 模块
    try:
        client.connect((ip, 9999))
        running = True
        t2 = Thread(target=Chatter.send, args=(client,))
        t1 = Thread(target=Chatter.recv, args=(client,t2))
        t1.start()
        t1.join()
        t2.join()
    except:     
        pass
    finally:
        print("连接已被关闭")
        #file.close()
        client.close()