import math
import random
from utils import long2bytes, bytes2long

def mod_inverse(a, m):
    """ 使用快速幂计算 a 在模 m 下的逆元 """
    a = a % m
    if a == 0:
        raise ValueError("Inverse does not exist")
    
    def fast_pow(base, exp, mod):
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result
    
    # 费马小定理：a^(m-2) ≡ a^(-1) (mod m)，前提是 m 是质数
    return fast_pow(a, m - 2, m)

class Point:
    def __init__(self, x, y, infinity=False, a=None, p=None):
        self.x = x
        self.y = y
        self.infinity = infinity
        self.a = a
        self.p = p

    def __eq__(self, other):
        if self.infinity and other.infinity:
            return True
        if self.infinity or other.infinity:
            return False
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return Point(self.x, -self.y % self.p, a=self.a, p=self.p)

    def __add__(self, other):
        if self.infinity:
            return other
        if other.infinity:
            return self
        if self == other:
            return self.double()
        if self.x == other.x:
            return Point(None, None, True, a=self.a, p=self.p)
        
        m = (other.y - self.y) * mod_inverse(other.x - self.x, self.p)
        x_r = (m**2 - self.x - other.x) % self.p
        y_r = (m * (self.x - x_r) - self.y) % self.p
        return Point(x_r, y_r, a=self.a, p=self.p)

    def double(self):
        if self.y == 0:
            return Point(None, None, True, a=self.a, p=self.p)
        m = (3 * self.x**2 + self.a) * mod_inverse(2 * self.y, self.p)
        x_r = (m**2 - 2 * self.x) % self.p
        y_r = (m * (self.x - x_r) - self.y) % self.p
        return Point(x_r, y_r, a=self.a, p=self.p)

    def __mul__(self, k):
        result = Point(None, None, True, a=self.a, p=self.p)
        addend = self
        while k:
            if k & 1:
                result += addend
            addend = addend.double()
            k >>= 1
        return result

class ECC_Cipher:
    def __init__(self, p=None, a=None, b=None, G=None, n=None):
        # 默认参数
        self.p = p or 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
        self.a = a or 0
        self.b = b or 7
        self.G = G or Point(55066263022277343669578718895168534326250603453777594175500187360389116729240,
                            32670510020758816978083085130507043184471273380659243275938904335757337482424,
                            a=self.a, p=self.p)
        self.n = n or 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        
        self.private_key, self.public_key = self.__generate_keys()

    def __generate_keys(self):
        d = random.randrange(self.n)
        Q = self.G * d
        return d, Q

    def encrypt(self, message, public_key):
        """
        使用ElGamal加密算法对消息进行加密。

        :param message: 需要加密的消息，通常为一个整数。
        :param public_key: 发送者的公钥，用于加密消息。
        :return: 返回一个元组，包含两个元素，第一个是加密密钥C1，第二个是加密后的消息。
        选择随机数r，将明文M生产密文C。密文是一个点对，C=(rP,M+rQ)
        """
        r = random.randrange(self.n)
        C1 = self.G * r
        C2 = public_key * r
        message = bytes2long(message)
        encrypted_message = (message + C2.x) % self.p
        encrypted_message = long2bytes(encrypted_message)
        return C1, encrypted_message

    def decrypt(self, C1, encrypted_message, private_key):
        """
        解密函数，用于将加密消息解密为原始消息。
        参数:
        - C1: 加密过程中使用的椭圆曲线点。
        - encrypted_message: 加密后的消息。
        - private_key: 解密所用的私钥。
        返回值:
        - message: 解密后的原始消息。
        encrypted_message-C1*private_key = M+rQ-k(rP)=M+r(kP)-K(rP)=M
        """
        C2 = C1 * private_key
        encrypted_message = bytes2long(encrypted_message)
        # 通过计算(加密消息 - C2的x坐标)模p来获取原始消息，这里p是椭圆曲线上的一个大素数
        message = (encrypted_message - C2.x) % self.p
        message = long2bytes(message)
        return message


if __name__ == '__main__':
    # 示例用法
    ecc_cipher = ECC_Cipher()
    print(f"Private Key: {ecc_cipher.private_key}")
    print(f"Public Key: ({ecc_cipher.public_key.x}, {ecc_cipher.public_key.y})")

    message = b'123456'
    C1, encrypted_message = ecc_cipher.encrypt(message, ecc_cipher.public_key)
    print(f"Encrypted Message: {encrypted_message}")

    decrypted_message = ecc_cipher.decrypt(C1, encrypted_message, ecc_cipher.private_key)
    print(f"Decrypted Message: {decrypted_message}")