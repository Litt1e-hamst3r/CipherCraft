import random
from .utils import generate_large_prime

class DiffieHellman:
    def __init__(self, p=None, g=None):
        """
        初始化Diffie-Hellman对象。
        
        :param p: 一个大的素数
        :param g: 一个小于p的整数，通常为生成元
        """
        if p is None or g is None:
            # 如果没有提供p和g，则使用默认值
            self.p = 23  # 小素数
            self.g = 5   # 生成元
        else:
            self.p = p
            self.g = g
        
        # 生成私钥
        self.private_key = self.__generate_private_key()
        # 计算公钥
        self.public_key = self.__generate_public_key(self.private_key)
    
    def __generate_private_key(self):
        """ 生成一个随机的私钥。"""
        # 私钥应该在1到p-1之间
        return random.randint(1, self.p - 1)
    
    def __generate_public_key(self, private_key):
        """
        使用给定的私钥计算公钥。
        
        :param private_key: 私钥
        :return: 公钥
        """
        return pow(self.g, private_key, self.p)
    
    def generate_shared_secret(self, other_public_key):
        """
        使用对方的公钥计算共享密钥。
        
        :param other_public_key: 对方的公钥
        :return: 共享密钥
        """
        return pow(other_public_key, self.private_key, self.p)

# 示例用法
if __name__ == "__main__":
    # 创建两个DiffieHellman实例
    p = generate_large_prime(1024)
    g = 3
    dh_alice = DiffieHellman(p, g)
    dh_bob = DiffieHellman(p, g)
    print(f"Alice's private key: {dh_alice.private_key}")
    print(f"Bob's private key: {dh_bob.private_key}")
    print(f"Alice's public key: {dh_alice.public_key}")
    print(f"Bob's public key: {dh_bob.public_key}")

    # 交换公钥
    shared_secret_alice = dh_alice.generate_shared_secret(dh_bob.public_key)
    shared_secret_bob = dh_bob.generate_shared_secret(dh_alice.public_key)

    print(f"Alice's shared secret: {shared_secret_alice}")
    print(f"Bob's shared secret: {shared_secret_bob}")