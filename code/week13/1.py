import socket,time
from threading import Thread

class Manager:
    def __init__(self,socket,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.socket=socket
        self.username = 'NA'

    def sendMsg(self,msg,username):
        try:
            self.socket.send(("%s %s: %s" %(self.getTime(), username, msg)).encode("utf-8"))
            return True
        except:
            return False

    def recv(self,mtu=1024):
        try:
            data = self.socket.recv(mtu).decode("utf-8")
            if data == "quit" or not data:
                return False
            return data
        except:
            return False
        
    def close(self):
        try:
            self.socket.close()
            return True
        except:
            return False

    def getId(self):
        return "%s-%s" % (self.ip,self.port)
    def getTime(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S"))

    def new_client(c):
        try:
            print("%s(%s) 尝试连接" %(c.ip,c.port))
            file = open('log.txt','a')
            file.write("%s(%s) 尝试连接\n" %(c.ip,c.port))
            data = c.recv()
            if not data:
                return
            c.username = data
            print("用户%s %s(%s)已连接" %(c.username,c.ip,c.port))
            file.write("用户%s %s(%s)已连接\n" %(c.username,c.ip,c.port))

            iports[c.username] = f'{c.ip}-{c.port}'
            c.socket.send("已连接".encode("utf-8"))
            while True:
                data = c.recv()
                if not data:
                    break
                elif data.split(' ')[0] == '@':
                    #c.sendMsg(data,c.username)
                    try:
                        clients[iports[data.split(' ')[1]]].sendMsg(data,c.username)
                    except Exception as e:
                        print("send error %s" % e)
                else:
                    print("用户%s %s(%s) 发送了: %s" % (c.username,c.ip, c.port, data))
                    file.write("用户%s %s(%s) 发送了: %s\n" % (c.username,c.ip, c.port, data))
                    Manager.broadcast(data,c.username)
        except socket.errno as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))
        finally:
            print("%s(%s) 断开连接" % (c.ip, c.port))
            file.write("%s(%s) 断开连接\n" % (c.ip, c.port))
            #file.close()
            c.close()
            clients.pop(c.getId())

    def broadcast(msg,username):
        for c in clients.values():
            c.sendMsg(msg,username)

def main(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    host = "127.0.0.1"
    server.bind((host, port))

    # 监听客户端
    server.listen(10)
    print("服务器已开启，正在监听{}".format(server.getsockname()))

    while True:
        # 接受客户端连接
        conn, addr = server.accept()
        c = Manager(conn,addr)
        clients[c.getId()] = c
        t = Thread(target=Manager.new_client, args=(c,))
        t.start()

if __name__ == "__main__":
    clients = {}
    iports = {}
    main(8080)
    print("服务器已关闭")