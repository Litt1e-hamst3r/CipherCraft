import sys
import os
# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from crypto.DH import DiffieHellman
from network import NetworkHandler

def get_DHkey_C(network_handler):
    # 接收p和g
    params = network_handler.receive_json()
    p = params['p']
    g = params['g']

    # 创建Diffie-Hellman实例
    dh = DiffieHellman(p, g)

    # 接收服务器的公钥
    data = network_handler.receive_json()
    server_public_key = data['public_key']

    # 发送自己的公钥
    network_handler.send_json({'public_key': dh.public_key})

    # 生成共享密钥
    shared_secret = dh.generate_shared_secret(server_public_key)
    return shared_secret

if __name__ == "__main__":
    network_handler = NetworkHandler('localhost', 22222)
    network_handler.connect('localhost', 12345)
    shared_secret = get_DHkey_C(network_handler)
    print(f"Shared secret: {shared_secret}")
    network_handler.close()