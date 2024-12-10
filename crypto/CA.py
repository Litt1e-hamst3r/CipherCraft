import numpy as np
from .utils import bin2bytes

class CA_Cipher:
    def __init__(self, seed, rule, key_position=0):
        assert 0 <= rule <= 255, "规则必须为0~255之间的整数"
        assert len(seed) > 0, "初始状态不能为空"
        assert 0 <= key_position < len(seed), "密钥位置必须在初始状态的范围内"
        self.seed = np.array(seed, dtype=int)   # 初始状态
        self.rule_binary = format(rule, '08b')  # 状态转移规则
        self.length = len(self.seed)            # 长度
        self.state = self.seed.copy()           # 当前状态
        self.key_position = key_position        # 密钥位置

    def __next_state(self):
        next_state = self.state.copy()
        for i in range(self.length):
            neighbors = [
                self.state[(i - 1) % self.length],  # 左邻居
                self.state[i],                      # 当前细胞
                self.state[(i + 1) % self.length]   # 右邻居
            ]

            # 将三个邻居状态转换为一个二进制数，然后根据规则计算下一个状态
            binary_str = ''.join(map(str, neighbors))
            decimal_value = int(binary_str, 2)

            # 下一个状态由规则的第 decimal_value 位决定（从右到左，最低位为第0位）
            next_state[i] = int(self.rule_binary[decimal_value])

        return next_state

    def __generate_keystream(self, length):
        keystream = np.zeros(length, dtype=int)
        for i in range(length):
            self.state = self.__next_state()  # 更新状态
            keystream[i] = self.state[self.key_position]  # 取指定位置的输出作为密钥
        self.state = self.seed.copy()       # 重置状态
        return keystream

    def encrypt(self, plaintext):
        plaintext_bits = np.array([int(b) for b in ''.join(format(c, '08b') for c in plaintext)])
        keystream = self.__generate_keystream(len(plaintext_bits))    # 生成密钥流
        ciphertext_bits = np.bitwise_xor(plaintext_bits, keystream)  # 异或
        bit_str = ''.join(map(str, ciphertext_bits))
        return bin2bytes(bit_str)

    def decrypt(self, ciphertext):
        # 解密过程与加密过程相同
        return self.encrypt(ciphertext)
 
# 示例使用
if __name__ == "__main__":
    seed = [0, 1, 1, 0, 1, 0, 1]    # 初始状态
    rule = 110                      # 状态转移规则
    key_position = 3                # 用户自定义的密钥位置

    plaintext = b"Hello, World!"      # 明文
    print(f"明文: {plaintext}")
    ca = CA_Cipher(seed, rule, key_position)
    print(f"rule: {ca.rule_binary}")
    ciphertext = ca.encrypt(plaintext)
    print(f"密文: {ciphertext.hex()}")

    decrypted_text = ca.decrypt(ciphertext)
    print(f"解密后的明文: {decrypted_text}")