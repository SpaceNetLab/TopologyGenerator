from multiprocessing import Process
import socket
import os

whoami = "S" #or "C"

def handle_client(client_socket):
    """
    处理客户端请求
    """
    while True:
        request_data = client_socket.recv(1024)
        if request_data.decode()[0] == "X":
            print("connection close")
            break
        print('recive:',request_data.decode()) #打印接收到的数据
        data = request_data.decode().split(",")
        return_data = ""
        print(data)
        if data[1][0] == whoami:
            command = "tc qdisc change dev eth0 root netem delay "+data[3]+"ms"
            os.system(command)
            return_data = "OK,"+request_data.decode()
        else:
            return_data = "ER,"+request_data.decode()
        client_socket.send(return_data.encode('utf-8')) #然后再发送数据
    client_socket.close()
    

if __name__== "__main__":
    os.system("tc qdisc del dev eth0 root")
    os.system("tc qdisc add dev eth0 root netem delay 50ms")

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost',9090)) #绑定要监听的端口
    server.listen(5) #开始监听 表示可以使用五个链接排队】

    print(whoami +" Started")

    while True:# conn就是客户端链接过来而在服务端为期生成的一个链接实例
        conn,addr = server.accept() #等待链接,多个链接的时候就会出现问题,其实返回了两个值
        print("[%s, %s]Client connected." % addr)
        handle_client_process = Process(target=handle_client, args=(conn,))
        handle_client_process.start()
    
    print(whoami +" Stopped")