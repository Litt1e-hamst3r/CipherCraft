import socket
import json

def start_server(host='0.0.0.0', port=6666):
    # 创建一个TCP/IP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定套接字到地址和端口
    server_socket.bind((host, port))
    
    # 开始监听传入的连接
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")
    
    # 等待连接(这里演示一次接收)
    connection, client_address = server_socket.accept()
    try:
        print(f"Connected by {client_address}")
        
        # 接收数据
        data = b''
        while True:
            part = connection.recv(1024)
            if not part:
                break
            data += part
        
        # 将接收到的字节串解码为字符串并解析JSON
        json_data = json.loads(data.decode())
        print(f"Received JSON data: {json_data}")
    
    finally:
        # 清理连接
        connection.close()

if __name__ == '__main__':
    start_server()