import math

class md5_Cipher:
    def __init__(self):
        """
        A、B、C、D四个初始状态变量
        R列表存储了每轮操作的旋转位数
        K列表存储了每轮操作的常量值
        """
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476
        self.R = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
        self.K = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xffffffff for i in range(64)]

    def F(self, x, y, z): return (x & y) | (~x & z)
    def G(self, x, y, z): return (x & z) | (y & ~z)
    def H(self, x, y, z): return x ^ y ^ z
    def I(self, x, y, z): return y ^ (x | ~z)

    # 循环左移函数
    def L(self, x, n): return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    
    # 重置状态变量
    def __reset(self):
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476

    # 填充消息并分块
    def __pad_message(self, msg):
        msg = bytearray(msg)
        length = len(msg) * 8

        msg.append(0x80)  # 添加1位的'1'（0x80）
        while (len(msg) * 8 + 64) % 512 != 0:  # 直到长度对512取模为448
            msg.append(0)

        # 添加消息长度的64位表示
        for i in range(8):
            msg.append((length >> (8 * i)) & 0xFF)

        return msg

    # 处理一个64字节大小的块
    def __process_chunk(self, chunk):
        a, b, c, d = self.A, self.B, self.C, self.D
        for i in range(64):
            if 0 <= i <= 15:
                f, g = self.F(b, c, d), i
            elif 16 <= i <= 31:
                f, g = self.G(b, c, d), (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f, g = self.H(b, c, d), (3 * i + 5) % 16
            else:
                f, g = self.I(b, c, d), (7 * i) % 16

            # 计算当前w值
            w = int.from_bytes(chunk[g*4:g*4+4], byteorder='little')

            # 主循环计算
            temp = (a + f + self.K[i] + w) & 0xFFFFFFFF
            a, b, c, d = d, (b + self.L(temp, self.R[i])) & 0xFFFFFFFF, b, c

        self.A = (self.A + a) & 0xFFFFFFFF
        self.B = (self.B + b) & 0xFFFFFFFF
        self.C = (self.C + c) & 0xFFFFFFFF
        self.D = (self.D + d) & 0xFFFFFFFF

    # 逆序字节序
    def __reverse_bytes(self, n):
        return int.from_bytes(n.to_bytes(4, byteorder='little'), byteorder='big')

    # 计算MD5哈希
    def digest(self, msg):
        # 填充消息并分块
        msg = self.__pad_message(msg)
        for i in range(0, len(msg), 64):
            chunk = msg[i:i + 64]
            self.__process_chunk(chunk)

        # 计算最终结果
        result = (self.__reverse_bytes(self.A) << 96) | (self.__reverse_bytes(self.B) << 64) | \
                 (self.__reverse_bytes(self.C) << 32) | self.__reverse_bytes(self.D)

        # 恢复初始状态
        self.__reset()

        # 返回32位小写十六进制字符串
        return f'{result:032x}'

# 示例用法
if __name__ == '__main__':
    cipher = md5_Cipher()
    print(cipher.digest(b"hello world"))  # 输出：5eb63bbbe01eeed093cb22bb8f5acdc3