import random
from .utils import bytes2long , long2bytes, mod_inverse, generate_large_prime

class RSA_Cipher:
    def __init__(self, public_key=None, private_key=None,key_size=None):
        self.key_size = key_size
        if (public_key is not None) and (private_key is not None):
            self.public_key = public_key
            self.private_key = private_key
        # 当没有设置，自动生成密钥对
        if key_size is not None:
            self.public_key, self.private_key = self.__generate_keys()

    def __generate_keys(self):
        p = generate_large_prime(self.key_size)
        q = generate_large_prime(self.key_size)
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