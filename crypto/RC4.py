import numpy as np

class RC4_Cipher:
    def __init__(self, key):
        self.key = key

    def KSA(self, key):
        """ 利用Key生成S盒 (KSA) """
        S = np.arange(256, dtype=np.uint8)
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def PRGA(self, S):
        """ 利用S盒生成密钥流 (PRGA) """
        i, j = 0, 0
        while True:
            i = (i + 1) % 256
            j = (j + int(S[i])) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(int(S[i]) + int(S[j])) % 256]
            yield K

    def encrypt(self, text):
        """ 加密就是密文和密钥流异或 """
        self.S = self.KSA(self.key)
        keystream = self.PRGA(self.S)
        res = np.fromiter((char ^ next(keystream) for char in text), dtype=np.uint8)
        return res.tobytes()

    def decrypt(self, ciphertext):
        """ 加密一样 """
        return self.encrypt(ciphertext)

if __name__ == "__main__":
    rc4 = RC4_Cipher(b"key")
    enc = rc4.encrypt(b"this is a test")
    print(enc)
    print(rc4.key)
    hex_enc = enc.hex()
    bytes_enc = bytes.fromhex(hex_enc)
    dec = rc4.encrypt(bytes_enc)
    print(dec.decode('utf-8'))