from .utils import bytes2bin, bin2bytes
import re


class DES_Cipher:
    # 置换选择表1(PC_1)
    PC_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

    # 选择压缩表2(PC_2)
    PC_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

    # 移位次数表
    SHIFT_NUM = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # 初始置换表IP
    IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

    # 逆置换表_IP
    _IP = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25 ]

    # 扩展置换表E
    E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

    # P盒
    P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

    S_BOX = [
        [  
            [ 14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7 ],
            [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8 ],
            [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0 ],
            [ 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ] 
        ],
        [  
            [ 15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10 ],
            [ 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5 ],
            [ 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15 ],
            [ 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ] 
        ],
        [  
            [ 10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8 ],
            [ 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1 ],
            [ 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7 ],
            [ 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ] 
        ],
        [  
            [ 7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15 ],
            [ 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9 ],
            [ 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4 ],
            [ 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 ] 
        ],
        [  
            [ 2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9 ],
            [ 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6 ],
            [ 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14 ],
            [ 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ] 
        ],
        [  
            [ 12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11 ],
            [ 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8 ],
            [ 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6 ],
            [ 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 ] 
        ],
        [  
            [ 4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1 ],
            [ 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6 ],
            [ 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2 ],
            [ 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12 ] 
        ],
        [  
            [ 13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7 ],
            [ 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2 ],
            [ 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8 ],
            [ 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11 ] 
        ] ,
    ]

    def __init__(self, key, mode='ECB'):
        """初始化"""
        self.key = key
        self.subkey_list = self.__generate_keys(key)

    def __generate_keys(self, key):
        """生成16轮的加解子密钥"""
        subkey_list = []  # 存储16轮子密钥
        # 1. 初始置换 64->58
        combined_key = [bytes2bin(key)[i - 1] for i in self.PC_1]
        # 2. 循环左移
        for i in self.SHIFT_NUM:
            key_left = combined_key[:28]
            key_right = combined_key[28:]
            key_left = key_left[i:] + key_left[:i]
            key_right = key_right[i:] + key_right[:i]
            combined_key = key_left  + key_right 
            subkey = ''.join([combined_key[i - 1] for i in self.PC_2])   # 生成子密钥
            subkey_list.append(subkey)  # 生成子密钥
        return subkey_list

    def __substitute(self, bin_data):
        """ S盒替换 """
        int_result = []
        result = ''
        for i in range(8):
            row = int(bin_data[i][0] + bin_data[i][5], 2)
            col = int(''.join(bin_data[i][j] for j in range(1, 5)), 2)
            int_result.append(self.S_BOX[i][row][col])
            # 十进制转成二进制
            result += bin(int_result[-1])[2:].zfill(4)
        return result

    def __f_function(self, R, bin_key):
        """轮函数"""
        # 将R由32位扩展成48位
        R_ext = [R[i - 1] for i in self.E]
        # 与子密钥进行逐位异或
        bin_temp = [str(int(r) ^ int(k)) for r, k in zip(R_ext, bin_key)]
        # 6个字符为一组
        bin_result = [''.join(bin_temp[i:i + 6]) for i in range(0, len(bin_temp), 6)]
        result = self.__substitute(bin_result)      # S盒替换
        result = ''.join(result[i - 1] for i in self.P)  # P盒置换
        return result

    def __des_cipher(self, bin_text, reverse_keys=False):
        """通用DES加密解密函数，根据 reverse_keys 参数判断加密还是解密"""
        # 初始置换IP
        bin_text = [bin_text[i - 1] for i in self.IP]
        # 分成左右两部分
        left_part, right_part = bin_text[:32], bin_text[32:]
        # 获得16轮子密钥
        subkey_list = self.subkey_list
        if reverse_keys:
            subkey_list = subkey_list[::-1]  # 解密时反转子密钥列表
        # 进行16轮迭代
        for i in subkey_list:
            right_part_temp = right_part
            # 轮函数f()结果和L进行异或
            right_part = ''.join(str(int(r) ^ int(l)) for r, l in zip(self.__f_function(right_part, i), left_part))
            left_part = right_part_temp
        # 进行IP-1逆置换 64->64
        bin_text = right_part + left_part
        result = ''.join(bin_text[i - 1] for i in self._IP)  # 进行IP-1逆置换
        return result  # 输出二进制字符串

    def encrypt(self, plaintext):
        """DES加密"""
        # 明文转成二进制字符串
        bin_plaintext = bytes2bin(plaintext)
        # 填充
        padding_len = (64 - (len(bin_plaintext) % 64)) % 64
        bin_padding_plaintext = bin_plaintext + '0' * padding_len
        # 进行64位分组加密
        bin_group = re.findall(r'.{64}', bin_padding_plaintext)
        bin_ciphertext = ''
        for g in bin_group:
            bin_ciphertext += self.__des_cipher(g)
        # 转成bytes输出
        return bin2bytes(bin_ciphertext)


    def decrypt(self, ciphertext):
        """DES解密"""
        # 进行64位分组加密
        bin_group = re.findall(r'.{64}', bytes2bin(ciphertext))
        bin_deciphertext = ''
        for g in bin_group:
            bin_deciphertext += self.__des_cipher(g, reverse_keys=True)
        # 转成bytes输出
        return bin2bytes(bin_deciphertext)


if __name__ == '__main__':
    plaintext = b'Hello, World!'
    key = b'12345678'
    """DES加密"""
    des = DES_Cipher(key)
    ciphertext = des.encrypt(plaintext)
    print(f'密文:{ciphertext}')
    # 密文:b'\x9a\xd0\xb4\xf8\xb6\xab`\x07\xae$\x80KP\x9e\xf8\t'
    print(f'解密:{des.decrypt(ciphertext)}')
    # 解密:b'Hello, World!\x00\x00\x00'