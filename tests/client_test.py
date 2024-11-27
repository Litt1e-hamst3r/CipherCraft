import socket
import json
import sys

def send_json_to_server(data, host='127.0.0.1', port=6666):
    # 创建一个TCP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 连接到服务器
    client_socket.connect((host, port))
    
    try:
        # 将数据转换为JSON格式的字符串
        json_data = json.dumps(data)
        
        # 发送数据
        client_socket.sendall(json_data.encode())
        print("Data sent successfully.")
    
    finally:
        # 关闭连接
        client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python client.py <data>")
    else:
        try:
            # 尝试将命令行参数解析为字典
            data = json.loads(sys.argv[1])
            send_json_to_server(data)
        except json.JSONDecodeError:
            print("Invalid JSON data provided.")