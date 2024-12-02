from network import NetworkHandler
import os
import sys
import random
# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from crypto.utils import generate_large_prime
from crypto.DH import DiffieHellman
from CipherProcessor import CipherProcessor
def get_DHkey_S(network_handler):
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

# # 由服务端生成RSA密钥对，发送公钥，保留私钥
def send_RSA_public_key(network_handler):
    public_key, private_key = CipherProcessor().process_auto_rsa("512")
    # 发送公钥
    network_handler.send_json({'public_key': public_key})
    # 保留私钥
    result = {'private_key': private_key}
    return result

def send_ECC_public_key(network_handler):
    size = random.randint(0, 512)
    public_key, private_key = CipherProcessor().process_auto_ecc(size)
    network_handler.send_json({'public_key': public_key})
    result = private_key
    return result

if __name__ == "__main__":
    # 创建网络处理器 服务器端口：localhost:12345
    network_handler = NetworkHandler('localhost', 12345)
    network_handler.socket.listen(1)

    # 接受连接
    client_socket, addr = network_handler.socket.accept()
    network_handler.socket = client_socket
    print(f"Server started on {network_handler.host}:{network_handler.port}")
    print(f"Connected to {addr}")

    # DH
    shared_secret = get_DHkey_S(network_handler)
    print(f"Shared secret: {shared_secret}")

    # RSA
    rsa_private_key = send_RSA_public_key(network_handler)

    # ECC (注意了如果有ECC要在发送 enc_data 前 先发送 C1)
    private_key = send_ECC_public_key(network_handler)
    print(f"Private key: {private_key}")
    C1 = network_handler.receive_bytes().decode()
    enc_data = network_handler.receive_bytes()
    cipherProcess = CipherProcessor(message=enc_data, json_list=['RSA', 'ECC']) # json_list 的顺序要和加密时的顺序相反
    key_list = [rsa_private_key, {'private_key': [C1, private_key]}]
    dec, _ = cipherProcess.easy_process(key_list, 'decrypt')
    print("Dec: ", dec)

    network_handler.close()