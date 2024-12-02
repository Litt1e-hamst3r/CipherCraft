# backend/network.py

import socket
import json

class NetworkHandler:
    def __init__(self, host=None, port=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host != None and port != None:   # 使用指定主机和端口
            self.host = host
            self.port = port
            self.socket.bind((self.host, self.port))

    def connect(self, host, port):
        """ 连接服务器(发送方需要的操作) """
        self.socket.connect((host, port))

    def send_json(self, data):
        """将Python字典转换为JSON字符串并发送给服务器"""
        try:
            json_data = json.dumps(data)
            self.socket.sendall(len(json_data).to_bytes(4, byteorder='big'))
            self.socket.sendall(json_data.encode('utf-8'))
        except Exception as e:
            print(f"Error sending data: {e}")
            raise

    def receive_json(self):
        """从服务器接收JSON格式的数据"""
        try:
            length_prefix = self.socket.recv(4)
            if not length_prefix:
                return None
            data_length = int.from_bytes(length_prefix, byteorder='big')
            
            received_data = bytearray()
            while len(received_data) < data_length:
                packet = self.socket.recv(data_length - len(received_data))
                if not packet:
                    break
                received_data.extend(packet)
            json_data = received_data.decode('utf-8')
            return json.loads(json_data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            raise

    def send_bytes(self, data):
        """ 发送原始字节数据 """
        try:
            self.socket.sendall(len(data).to_bytes(4, byteorder='big'))
            self.socket.sendall(data)
        except Exception as e:
            print(f"Error sending bytes: {e}")
            raise

    def receive_bytes(self):
        """ 接收原始字节数据 """
        try:
            length_prefix = self.socket.recv(4)
            if not length_prefix:
                return None
            data_length = int.from_bytes(length_prefix, byteorder='big')
            
            received_data = bytearray()
            while len(received_data) < data_length:
                packet = self.socket.recv(data_length - len(received_data))
                if not packet:
                    break
                received_data.extend(packet)
            
            return bytes(received_data)
        except Exception as e:
            print(f"Error receiving bytes: {e}")
            raise

    def close(self):
        """ 关闭套接字 """
        self.socket.close()