import sys
import os
# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from crypto.DH import DiffieHellman
from network import NetworkHandler
from CipherProcessor import CipherProcessor

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

# # 接收RSA公钥
def receive_RSA_public_key(network_handler):
    data = network_handler.receive_json()
    return data

def receive_ECC_public_key(network_handler):
    data = network_handler.receive_json()
    return data

if __name__ == "__main__":
    network_handler = NetworkHandler()
    network_handler.connect('localhost', 12345)

    shared_secret = get_DHkey_C(network_handler)
    print(f"Shared secret: {shared_secret}")

    msg = b'1234567890qwertyuio'
    # RSA
    rsa_public_key = receive_RSA_public_key(network_handler)
    # ECC
    public_key = receive_ECC_public_key(network_handler)
    cipherProcess = CipherProcessor(message=msg, json_list=['ECC', 'RSA'])
    print(f"Public key: {public_key}")
    key_list = [public_key, rsa_public_key]
    data, C1 = cipherProcess.easy_process(key_list, 'encrypt')
    # 先发送 C1
    network_handler.send_bytes(C1.encode())
    # 再发送 enc_data
    network_handler.send_bytes(data)
    print(data)
    network_handler.close()