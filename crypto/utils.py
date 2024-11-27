import re
import numpy as np
import random

def str2bin(text):
    """字符串转二进制字符串"""
    return ''.join(bin(byte)[2:].zfill(8) for byte in text.encode())

def bin2str(bit_str):
    """二进制字符串转字符串"""
    # 1.将二进制字符串按8位分割，并转换为字节数组
    byte_array = ''.join(chr(int(bit_str[i:i+8], 2)) for i in range(0, len(bit_str), 8))
    # 2.将字节序列解码为字符串
    return byte_array

def hex2bin(hex_str):
    """十六进制字符串转二进制字符串"""
    return ''.join(bin(int(h, 16))[2:].zfill(4) for h in hex_str)

def bin2hex(bin_str):
    """二进制字符串转十六进制字符串"""
    return ''.join(hex(int(bin_str[i:i+4], 2))[2:].zfill(2) for i in range(0, len(bin_str), 4))

def bytes2bin(byte_data):
    """字节串转二进制字符串"""
    return ''.join(bin(byte)[2:].zfill(8) for byte in byte_data)

def bin2bytes(bin_str):
    """二进制字符串转字节串"""
    # 1. 将二进制字符串按8位分割，并转换为整数列表
    byte_list = [int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8)]
    # 2. 将整数列表转换为字节串
    return bytes(byte_list)

def long2bytes(n, byteorder='big'):
    """
    将长整数转换为字节字符串。
    """
    # 计算所需的字节数
    length = (n.bit_length() + 7) // 8
    # 使用 int.to_bytes 方法进行转换
    return n.to_bytes(length, byteorder)

def bytes2long(byte_string, byteorder='big'):
    """
    将字节字符串转换为长整数。
    """
    return int.from_bytes(byte_string, byteorder)

def mod_inverse(a, m):
    """计算 a 在模 m 下的逆元"""
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def is_prime(n, k=5):
    """
    Miller-Rabin 素性检验算法
    n: 待检测的数
    k: 进行素性检验的迭代次数，默认为5次
    返回: True 如果 n 是素数，False 如果 n 不是素数
    """
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:    # 排除一些简单的
        return False

    # 将 n - 1 表示为 2^s * d 的形式
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # 进行 k 次独立的素性检验
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # x = a^d % n
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)  # x = x^2 % n
            if x == n - 1:
                break
        else:
            return False  # 如果没有找到合适的 x，则 n 不是素数
    return True

def generate_large_prime(key_size):
    while True:
        num = random.getrandbits(key_size)
        if is_prime(num):
            return num

if __name__ == '__main__':
    # 示例长整数
    n = 123456789

    # 转换为字节字符串
    byte_string = long2bytes(n)

    print(f"Long Integer: {n}")
    print(f"Byte String: {byte_string}")
    print(f"Converted Long Integer: {bytes2long(byte_string)}")