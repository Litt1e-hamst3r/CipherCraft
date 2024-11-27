import random
from utils import bytes2long , long2bytes, mod_inverse

class RSA_Cipher:
    def __init__(self, public_key=None, private_key=None,key_size=1024):
        self.key_size = key_size
        if (public_key is not None) and (private_key is not None):
            self.public_key = public_key
            self.private_key = private_key
        # 当没有设置，自动生成密钥对
        self.public_key, self.private_key = self.__generate_keys()


    def __is_prime(self, n, k=5):
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

    def __generate_large_prime(self):
        while True:
            num = random.getrandbits(self.key_size)
            if self.__is_prime(num):
                return num

    def __generate_keys(self):
        p = self.__generate_large_prime()
        q = self.__generate_large_prime()
        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = 65537
        d = mod_inverse(e, phi_n)
        return (n, e), (n, d)

    def __fast_exponentiation(self, base, exponent, modulus):
        """
        快速幂取模算法。
        计算结果 (base^exponent) % modulus
        """
        result = 1
        base = base % modulus
        
        while exponent > 0:
            # 如果当前指数是奇数，将当前结果乘以当前底数并取模
            if exponent % 2 == 1:
                result = (result * base) % modulus
            # 将指数右移一位，相当于整除2
            exponent = exponent >> 1
            # 将底数平方并取模
            base = (base * base) % modulus
        return result

    def encrypt(self, plaintext, public_key):
        n, e = public_key
        plaintext = bytes2long(plaintext)
        ciphertext = self.__fast_exponentiation(plaintext, e, n)
        ciphertext = long2bytes(ciphertext)
        return ciphertext

    def decrypt(self, ciphertext, private_key):
        n, d = private_key
        ciphertext = bytes2long(ciphertext)
        plaintext = self.__fast_exponentiation(ciphertext, d, n)
        plaintext = long2bytes(plaintext)
        return plaintext

# Example usage
if __name__ == "__main__":
    rsa = RSA_Cipher(key_size=1024)
    public_key, private_key = rsa.public_key, rsa.private_key
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    plaintext = b'123456789'
    ciphertext = rsa.encrypt(plaintext, public_key)
    decrypted_text = rsa.decrypt(ciphertext, private_key)

    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted Text: {decrypted_text}")