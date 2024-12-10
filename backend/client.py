import sys
import os
from .Key import get_key_from_integer

# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from crypto.DH import DiffieHellman
from .network import NetworkHandler
from .CipherProcessor import CipherProcessor

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

# 接收RSA公钥
def receive_RSA_public_key(network_handler):
    data = network_handler.receive_json()
    return data

def receive_ECC_public_key(network_handler):
    data = network_handler.receive_json()
    return data

def generate_error(error_code, error_message):
    return {"error_code": error_code, "error_message": error_message}

def send_once(self_port, ip, port, msg, algorithm_list):
    try:
        network_handler = NetworkHandler()
        network_handler.connect(ip, port)
        # self_port
        network_handler.send_json({'port': self_port})
        # DH
        shared_secret = get_DHkey_C(network_handler)
        # 发送 algorithm_list
        network_handler.send_json(algorithm_list)
        # RSA
        rsa_public_key = receive_RSA_public_key(network_handler)
        # ECC
        ecc_public_key = receive_ECC_public_key(network_handler)
        # 算法列表
        key_list = []
        for algorithm in algorithm_list:
            if algorithm == 'ECC':
                key_list.append(ecc_public_key)
            elif algorithm == 'RSA':
                key_list.append(rsa_public_key)
            else: 
                key_list.append(get_key_from_integer(shared_secret, algorithm))
        print("key_list", key_list)
        cipherProcess = CipherProcessor(message=msg, json_list=algorithm_list)
        data, C1 = cipherProcess.easy_process(key_list, 'encrypt')
        # 先发送 C1
        network_handler.send_bytes(C1.encode())
        # 再发送 enc_data
        network_handler.send_bytes(data)
        # print(data)
        network_handler.close()
        return data
    except Exception as e:
        return generate_error(-2, str(e))

if __name__ == "__main__":
    error = send_once('127.0.0.1', 12345, '你好啊'.encode(), ['Caesar'])
    print(error)