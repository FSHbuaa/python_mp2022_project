from socket import *
from threading import Thread
import time
import sys

HOST='127.0.0.1'
PORT = 9999

class Manager:
    def __init__(self,socket,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.socket=socket
        self.username = 'NA'                            #不会被采用的临时username
        self.id = str(self.ip)+'('+str(self.port)+')'   #每个对接的用户的主键
    
    def send_msg(self,msg,username):
        try:
            self.socket.send(("%s %s: %s" %(str(time.strftime("%Y-%m-%d %H:%M:%S")), username, msg)).encode("utf-8"))
            return True
        except Exception as e:
            print("send error %s" % e)
            return False
    
    def recv_msg(self):
        try:
            data = self.socket.recv(1024).decode("utf-8")
            if data == "quit" or not data:
                return False
            return data
        except:
            return False

    def broadcast(self,msg,username):
        for c in clients.values():
            c.send_msg(msg,username)        

    def connect_client(self):
        try:
            print(f"{self.id} 尝试连接")
            file = open('log.txt','a')
            file.write(f"{self.id}尝试连接\n")
            data = self.recv_msg()
            if not data:
                return
            self.username = data
            print(f"用户{self.username} {self.id}已连接")
            file.write(f"用户{self.username} {self.id}已连接\n")
            iports[self.username] = self.id
            self.socket.send("已连接".encode("utf-8"))
            while True:
                data = self.recv_msg()
                if not data:
                    break
                elif data.split(' ')[0] == '@':
                    try:
                        data_lis = data.split(' ')
                        username_tmp = data_lis[1]
                        data_new=''
                        for i in range(2,len(data_lis)):
                            data_new += data_lis[i]
                        clients[iports[username_tmp]].send_msg(data_new,self.username)
                    except Exception as e:
                        print("send error %s" % e)
                else:
                    print(f"用户{self.username} {self.id}发送了: {data}")
                    file.write(f"用户{self.username} {self.id} 发送了: {data}\n")
                    self.broadcast(data,self.username)
        except Exception as e:
            print("Exception: %s" % str(e))
        finally:
            print(f"{self.id} 断开连接")
            file.write(f"{self.id} 断开连接\n")
            file.close()
            self.socket.close()
            clients.pop(self.id)

class Chatter:
    def __init__(self,ip,port,username):
        """
        在初始化中完成多线程的收发消息
        """
        self.file = open(username+'.txt','a')
        self.file.write('username 聊天记录\n')
        client = socket(AF_INET,SOCK_STREAM)
        try:
            client.connect((ip,port))
            self.R = True
            t1 = Thread(target=self.send_msg, args=(client,self.file))
            t2 = Thread(target=self.recv_msg, args=(client,self.file))
            client.send(username.encode("utf-8"))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        except Exception as e:   
            print("client error %s" % e)
        finally:
            print("连接已被关闭")
            self.file.close()
            client.close()

    def send_msg(self,c,file):
        time.sleep(0.5)
        while True:
            data = input('')
            c.send(data.encode("utf-8"))
            file.write(data+'\n')
            if data == "quit":
                self.R = False
                break
    
    def recv_msg(self,c,file):
        while self.R:
            try:
                data = c.recv(1024).decode("utf-8")
                if not data:
                    break
                print(data)
                file.write(data+'\n')
            except Exception as e:
                print("recv error %s" % e)

if __name__ == "__main__":
    if sys.argv[1] == 'client':
        Client = Chatter(HOST,PORT,sys.argv[2])
    elif sys.argv[1] == 'server':
        clients = {}
        iports = {}
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        server.bind((HOST,PORT))
        server.listen(10)
        print("服务器已开启，正在监听{}".format(server.getsockname()))
        while True:
            conn, addr = server.accept() #在此阻塞
            c = Manager(conn,addr)
            clients[c.id] = c
            t = Thread(target=Manager.connect_client, args=(c,))
            t.start()