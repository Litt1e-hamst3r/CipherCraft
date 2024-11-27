from network import NetworkHandler
import os
import sys
# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from crypto.utils import generate_large_prime
from crypto.DH import DiffieHellman
def get_DHkey_S(network_handler):
    # 接受连接
    client_socket, addr = network_handler.socket.accept()
    network_handler.socket = client_socket

    # 协商p和g
    p = generate_large_prime(1024)
    g = 3
    network_handler.send_json({'p': p, 'g': g})

    # 创建Diffie-Hellman实例
    dh = DiffieHellman(p, g)

    # 发送公钥
    network_handler.send_json({'public_key': dh.public_key})

    # 接收客户端的公钥
    data = network_handler.receive_json()
    client_public_key = data['public_key']

    # 生成共享密钥
    shared_secret = dh.generate_shared_secret(client_public_key)
    return shared_secret

if __name__ == "__main__":
    # 创建网络处理器
    network_handler = NetworkHandler('127.0.0.1', 12345)
    network_handler.socket.listen(1)
    print(f"Server started on {network_handler.host}:{network_handler.port}")
    shared_secret = get_DHkey_S(network_handler)
    print(f"Shared secret: {shared_secret}")
    network_handler.close()