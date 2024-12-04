from .network import NetworkHandler
import os
import sys
import random
from .Key import get_key_from_integer
# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from crypto.utils import generate_large_prime
from crypto.DH import DiffieHellman
from .CipherProcessor import CipherProcessor
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

def generate_error(error_code, error_message):
    return {"error_code": error_code, "error_message": error_message}

def receive_once(network_handler):
    try:
        # self_port
        target_port = network_handler.receive_json()
        target_port = target_port['port']

        # DH
        shared_secret = get_DHkey_S(network_handler)
        # 接受 algorithm_list
        algorithm_list = network_handler.receive_json()
        # RSA
        rsa_private_key = send_RSA_public_key(network_handler)
        # ECC (注意了如果有ECC要在发送 enc_data 前 先发送 C1)
        ecc_private_key = send_ECC_public_key(network_handler)
        C1 = network_handler.receive_bytes().decode()
        key_list = []
        for algorithm in algorithm_list:
            if algorithm == 'ECC':
                key_list.append({'private_key': [C1, ecc_private_key]})
            elif algorithm == 'RSA':
                key_list.append(rsa_private_key)
            else: 
                key_list.append(get_key_from_integer(shared_secret, algorithm))

        print("key_list", key_list)
        # 逆向密钥
        algorithm_list.reverse()
        key_list.reverse()
        enc_data = network_handler.receive_bytes()
        cipherProcess = CipherProcessor(message=enc_data, json_list=algorithm_list) # json_list 的顺序要和加密时的顺序相反
        dec, _ = cipherProcess.easy_process(key_list, 'decrypt')
        
        return target_port, dec
    except Exception as e:
        return generate_error(-2, str(e))

if __name__ == "__main__":
    while True:
        # 接受连接
        # 创建网络处理器 服务器端口：localhost:12345
        ip, port = '0.0.0.0', 12345
        while True:
            try:
                network_handler = NetworkHandler(ip, port)
                break
            except Exception as e:
                port += 1
        network_handler.socket.listen(1)
        client_socket, addr = network_handler.socket.accept()
        network_handler.socket = client_socket
        print(f"Server started on {network_handler.host}:{network_handler.port}")
        print(f"Connected to {addr}")
        dec = receive_once(network_handler)
        print(dec.decode())