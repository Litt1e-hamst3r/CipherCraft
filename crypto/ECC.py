import random
from .utils import long2bytes, bytes2long

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
        """ 参数:
        - x: 点的x坐标
        - y: 点的y坐标
        - infinity: 是否代表无穷远点，默认为False
        - a: 椭圆曲线参数a，默认为None
        - p: 椭圆曲线所在的有限域的特征，默认为None
        """
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
        """ 用于计算点的逆元(即对称的点) """
        return Point(self.x, -self.y % self.p, a=self.a, p=self.p)

    def __add__(self, other):
        """
        定义椭圆曲线上两点的加法运算。
        - 返回一个新点，该点是self和other在椭圆曲线上的加法结果。
        """
        # 如果当前点是无穷远点，则返回其他点。
        if self.infinity:
            return other
        # 如果其他点是无穷远点，则返回当前点。
        if other.infinity:
            return self
        # 如果当前点和其他点相同，则执行点的倍乘操作。
        if self == other:
            return self.double()
        # 如果当前点和其他点的x坐标相同，说明它们在垂直于x轴的直线上，结果为无穷远点。
        if self.x == other.x:
            return Point(None, None, True, a=self.a, p=self.p)
        
        # 计算两点连线的斜率m。
        m = (other.y - self.y) * mod_inverse(other.x - self.x, self.p)
        # 根据斜率m计算结果点的x坐标。
        x_r = (m**2 - self.x - other.x) % self.p
        # 根据斜率m和x坐标计算结果点的y坐标。
        y_r = (m * (self.x - x_r) - self.y) % self.p
        # 返回结果点。
        return Point(x_r, y_r, a=self.a, p=self.p)
    
    def double(self):
        """
        实现椭圆曲线上的点倍乘操作。
        返回：一个新的Point实例，表示当前点的两倍点。
        """
        # 当前点为无穷远点时，返回一个新的无穷远点
        if self.y == 0:
            return Point(None, None, True, a=self.a, p=self.p)
        
        # 计算切线的斜率m
        m = (3 * self.x**2 + self.a) * mod_inverse(2 * self.y, self.p)
        
        # 计算倍乘结果点的x坐标和y坐标
        x_r = (m**2 - 2 * self.x) % self.p
        y_r = (m * (self.x - x_r) - self.y) % self.p
        
        # 返回新的Point实例，表示当前点的两倍点
        return Point(x_r, y_r, a=self.a, p=self.p)

    def __mul__(self, k):
        """
        实现点的标量乘法操作，即计算椭圆曲线上的一个点与一个整数的乘积。
        结果是一个新的点，表示原始点与整数k的乘积。
        """
        # 初始化结果为无穷远点，为后续的点加法做准备
        result = Point(None, None, True, a=self.a, p=self.p)
        # 设置加数为当前点，用于在循环中进行点的倍乘操作
        addend = self
        
        # 当k不为0时，执行循环
        while k:
            # 如果k的最低位为1，将当前加数加入到结果中
            if k & 1:
                result += addend
            # 对加数进行倍乘操作，即计算当前点的两倍点
            addend = addend.double()
            # 右移k的二进制表示，为下一轮循环做准备
            k >>= 1
        
        # 返回最终的乘法结果点
        return result

    def __str__(self):
        if self.infinity:
            return f"Infinity(a={self.a},p={self.p})"
        return f"({self.x},{self.y},a={self.a},p={self.p})"

    @classmethod
    def from_string(cls, s):
        if s.startswith("Infinity"):
            _, a, p = s.split('(')[1].split(')')[0].split(',')
            a = int(a.split('=')[1])
            p = int(p.split('=')[1])
            return cls(None, None, infinity=True, a=a, p=p)
        else:
            x, y, a, p = s.strip('()').split(',')
            x = int(x)
            y = int(y)
            a = int(a.split('=')[1])
            p = int(p.split('=')[1])
            return cls(x, y, a=a, p=p)

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
        使用 ElGamal 加密算法对消息进行加密。
        选择随机数r，将明文M生产密文C。密文是一个点对，C=(rP,M+rQ)
        """
        r = random.randrange(self.n)
        C1 = self.G * r
        C2 = public_key * r
        # message的长度不能大于31字节
        if len(message) > 31:
            raise ValueError("Message length cannot exceed 32 bytes")
        message = bytes2long(message)
        # 通过计算(加密消息 + public_key * r)模p来获取原始消息
        encrypted_message = (message + C2.x) % self.p
        encrypted_message = long2bytes(encrypted_message)
        return C1, encrypted_message

    def decrypt(self, C1, encrypted_message, private_key):
        """
        解密函数，用于将加密消息解密为原始消息。
        encrypted_message-C1*private_key = M+rQ-k(rP)=M+r(kP)-K(rP)=M
        """
        C2 = C1 * private_key
        encrypted_message = bytes2long(encrypted_message)
        # 通过计算(加密消息 - C1*private_key)模p 来获取原始消息
        message = (encrypted_message - C2.x) % self.p
        message = long2bytes(message)
        return message


if __name__ == '__main__':
    # # 示例用法
    ecc_cipher = ECC_Cipher()
    print(f"Private Key: {ecc_cipher.private_key}")
    print(f"Public Key: ({ecc_cipher.public_key.x}, {ecc_cipher.public_key.y})")

    message = b'\xFF'*31
    C1, encrypted_message = ecc_cipher.encrypt(message, ecc_cipher.public_key)
    print(f"Encrypted Message: {encrypted_message}")

    decrypted_message = ecc_cipher.decrypt(C1, encrypted_message, ecc_cipher.private_key)
    print(f"Decrypted Message: {decrypted_message}")