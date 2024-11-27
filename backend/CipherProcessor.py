import sys
import os
import json
import base64

# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from crypto import AES, RSA, ECC, md5, CA, DES, DH, RC4, utils

class CipherProcessor:
    def __init__(self, message ,json_list):
        self.message = message
        self.json_list = json_list

    def __generate_error(self, error_code, error_message):
        return {"error_code": error_code, "error_message": error_message}

    # 到达 process 的默认 key/input/output 类型为 bytes
    def process_aes(self, message, key, mode):
        # 判断 key 是否是 128 比特
        if len(key) != 16:
            return self.__generate_error(-1, "key 应该为 128 比特")
        aes = AES.AES_Cipher(key)
        if mode == 'encrypt':
            return aes.encrypt(message)
        elif mode == 'decrypt':
            return aes.decrypt(message)
        
    def process_des(self, message, key, mode):
        # 判断 key 是否是 64 比特
        if len(key) != 8:
            return self.__generate_error(-1, "key 应该为 64 比特")
        des = DES.DES_Cipher(key)
        if mode == 'encrypt':
            return des.encrypt(message)
        elif mode == 'decrypt':
            return des.decrypt(message)
        
    def process_rc4(self, message, key, mode):
        rc4 = RC4.RC4_Cipher(key)
        if mode == 'encrypt':
            return rc4.encrypt(message)
        elif mode == 'decrypt':
            return rc4.decrypt(message)
        
    def process_ca(self, message, seed_str, rule, key_position, mode):
        seed = [int(char) for char in seed_str]
        # 检查输入是否有效
        if not 0 <= rule <= 255:
            return self.__generate_error(-1, "规则必须为0~255之间的整数")
        if len(seed) == 0:
            return self.__generate_error(-1, "初始状态不能为空")
        if not 0 <= key_position < len(seed):
            return self.__generate_error(-1, "密钥位置必须在初始状态的范围内")
        for s in seed:
            if not (s == 0 or s == 1):
                return self.__generate_error(-1, "初始状态必须为二进制字符串")
        # 加解密操作
        ca = CA.CA_Cipher(seed, rule, key_position)
        if mode == 'encrypt':
            return ca.encrypt(message)
        elif mode == 'decrypt':
            return ca.decrypt(message)
    
    def process_auto_rsa(self, key_size):
        if not isinstance(key_size, int):
            return self.__generate_error(-1, "密钥长度必须为整数")
        if key_size > 1025:
            return self.__generate_error(-1, "运算能力有限，密钥长度不能大于1024")
        rsa = RSA.RSA_Cipher(key_size=key_size)
        return rsa.public_key, rsa.private_key

    def process_rsa(self, message, key, mode):
        # Public Key: (5708751645665551867988435152295042002900656546814553562041790661173395267160248203346275226981729274863105380309285835952807135013601370346078591073582583529528777035596033899947333849233579054287395304806433156810891837380513341619168460505888024298450690969236484899201270631040777802394807920034031430982794691990129085669592046187690317179882739350521855060618276724101196481699568217618711733853210827562811314817570422438458498488137512019648200185253897061002824402403336883504764504589813710645012629541544073690174787466362853561503931300047741559673259683930396343722405675874948276681584703141580483222549, 65537)
        # Private Key: (5708751645665551867988435152295042002900656546814553562041790661173395267160248203346275226981729274863105380309285835952807135013601370346078591073582583529528777035596033899947333849233579054287395304806433156810891837380513341619168460505888024298450690969236484899201270631040777802394807920034031430982794691990129085669592046187690317179882739350521855060618276724101196481699568217618711733853210827562811314817570422438458498488137512019648200185253897061002824402403336883504764504589813710645012629541544073690174787466362853561503931300047741559673259683930396343722405675874948276681584703141580483222549, 184144849152951411400087765871976422389367653996459499674326646897486268745544725908632159388427539970712800005704110002048221362264877808132965218572006371689638443219097848001719086276146087260075280747681457703255036761255553415367229588010547986128824339059858233927575050948627558085701572286676876346144800344338008863542375097274838749799513348550503671887379451170281048072946668685939526194414220881910147834266260992160593547969950988909181121505987090963773282862486589447320339199003793216976535148438367375870417114174476893651881569160971653939225518232529726365557243458159760565428907293164933138881)
        # Plaintext: b'123456789'
        # Ciphertext: b'\xe0\xc2\xd3$f\xcb\xd5]\x1b\'\x98\xdf)\xf1\xf2N9\xcb\x1d\xa2x\xc4\xe2\xef\x11\xdb\xcc\xce\x89\xe3c\x9d\xb5X\xad\x87us\x9e\xd2#\\je\x11\x95\x1b\xb1\xa2\xfb\x97sPD\x16\x06\x03\x92\x1f\x04\x9a\xc8\xed\xe9\xd6vh\xc6X\xa94\xdb\xd8in\x81\xe2\xa0\xf5\x14\xafA9\xba\x17\x1e\xf5\xeb\xa3\xfb\xde2=Nh(Q6|\xb4\xbe\x96\x82\xf4\x1fK\xd5;\xa9\x91\x9d\t\xbfF\xc6\x10\x825\xac)\xfd0\x19o\xda@\xab@N\xf7\xd1z\xdd\xd5\xa2\x8f\xb2p\x98\x07u\xdf\x84"\x8c\xf1\x16\xca\xf1\x92R\xf1\x10\xeba\xe1\xed\xa6@\xe4\x82A\xbb\x8a\x88X\x14\xff@F\xa8\x89\xa6\x8ao\xcf\xb0\xf7\xb9\x95\x15\xa8\x97\xdc\xb6\x95\xcd(\xe4\x95\x8c\xe9z\xff=\xe8\x8d\x8aT\x05\xeb\xc8\xb1\xa7\x9cy\xfb;h\x19W\xd3R\xb8:\x1f\xdb\x83\xee?\x13\x07NN\xa3/rT\tq\xaeh\x81P\x92\x96t\xc0\x85$\xf9\xb5W$\x92c\x16\x94\xb3a\xde\xbc\xda\xbb\x1f'
        # Decrypted Text: b'123456789'
        rsa = RSA.RSA_Cipher()
        if mode == 'encrypt':
            return rsa.encrypt(message, key)
        elif mode == 'decrypt':
            return rsa.decrypt(message, key)

    def process_auto_ecc(self, a, b):
        ecc = ECC.ECC_Cipher(a=a, b=b)
        return ecc.public_key, ecc.private_key

    def process_ecc(self, message, key, mode, may_c1=None):
        ecc = ECC.ECC_Cipher()
        if mode == 'encrypt':
            c1, encrypted_message = ecc.encrypt(message, key)
            return [str(c1), encrypted_message]
        elif mode == 'decrypt':
            return ecc.decrypt(may_c1, message, key)
        
    def process_md5(self, message):
        m = md5.md5_Cipher()
        return m.digest(message)
    
    def process(self):
        
        for json_part in self.json_list:
            # {
            #     "algorithm": "Caesar", 
            #     "key": ["key"],
            #     "mode": "encrypt",  
            #     "key_type": "hex",
            #     "input_type": "hex",
            #     "output_type": "hex"
            # }
            key = b""
            # 统一key
            if json_part['key_type'] == 'hex':
                key = bytes.fromhex(json_part['key'][0])
            elif json_part['key_type'] == 'str':
                key = json_part['key'][0].encode()
            else: key = json_part['key']
            # 统一input
            if json_part['input_type'] == "hex":
                self.message = bytes.fromhex(self.message)
            elif json_part['input_type'] == "str":
                self.message = self.message.encode()

            # 根据算法选择加密方式
            alogorithm = json_part['algorithm']
            mode = json_part['mode']
            if alogorithm == 'AES': result = self.process_aes(self.message, key, mode)
            elif alogorithm == 'DES': result = self.process_des(self.message, key, mode)
            elif alogorithm == 'RC4': result = self.process_rc4(self.message, key, mode) 
            elif alogorithm == 'RSA': result = self.process_rsa(self.message, key, mode)
            elif alogorithm == 'ECC': 
                result = self.process_ecc(self.message, key, mode)
                self.message = result
                return result   # 由于是一个 list 列表，所以直接返回
            elif alogorithm == 'MD5': result = self.process_md5(self.message)
            # CA 比较特殊
            elif alogorithm == 'CA': 
                seed_str = key[0]
                rule = key[1]
                key_position = key[2]
                result = self.process_ca(self.message, seed_str, rule, key_position, mode)
            # 判断 result 是否为 {"error_code": error_code, "error_message": error_message} 格式
            if isinstance(result, dict) and 'error_code' in result and 'error_message' in result:
                return result
            # result 是 bytes 类型
            if json_part['output_type'] == 'hex':
                self.message = result.hex()
            elif json_part['output_type'] == 'str':
                self.message = result.decode()
            elif json_part['output_type'] == 'base64':
                self.message = base64.b64encode(result).decode()
            else:
                self.message = result
            # 输出解密结果
        return self.message
            


if __name__ == '__main__':

    message = "Hello, World!"
    # AES
    # json_list = [
    #     {
    #         "algorithm": "AES",
    #         "key": ["1234567890123456"],  # 16字节的密钥
    #         "mode": "encrypt",
    #         "key_type": "str",
    #         "input_type": "str",
    #         "output_type": "hex"
    #     },
    #     {
    #         "algorithm": "AES",
    #         "key": ["1234567890123456"],  # 16字节的密钥
    #         "mode": "decrypt",
    #         "key_type": "str",
    #         "input_type": "hex",
    #         "output_type": "str"
    #     }
    # ]

    RSA
    cipher = CipherProcessor("","")
    public_key, private_key = cipher.process_auto_rsa(1024)
    json_list = [
        {
            "algorithm": "RSA",
            "key": public_key,  # 16字节的密钥
            "mode": "encrypt",
            "key_type": "",
            "input_type": "str",
            "output_type": "hex"
        },
        {
            "algorithm": "RSA",
            "key": private_key,  # 16字节的密钥
            "mode": "decrypt",
            "key_type": "",
            "input_type": "hex",
            "output_type": "str"
        }
    ]

    cipher_processor = CipherProcessor(message, json_list)
    encrypted_message = cipher_processor.process()
    print(f"Encrypted Message: {encrypted_message}")
    
    
    # RSA
    # public_key, private_key = cipher.process_auto_rsa(1024)
    # print(f"Public Key: {public_key}")
    # print(f"Private Key: {private_key}")
    # plaintext = b"hello world"
    # ciphertext = cipher.process_rsa(plaintext, public_key, "encrypt")
    # decrypted_text = cipher.process_rsa(ciphertext, private_key, "decrypt")
    # print(f"Plaintext: {plaintext}")
    # print(f"Ciphertext: {ciphertext}")
    # print(f"Decrypted Text: {decrypted_text}")

    # ECC
    # public_key, private_key = cipher.process_auto_ecc(0,7)
    # print(f"Private Key: {private_key}")
    # print(f"Public Key: ({public_key.x}, {public_key.y})")
    # message = b'123456'
    # a = cipher.process_ecc(message, public_key, "encrypt")
    # C1, encrypted_message = a[0], a[1]
    # print(f"C1: {json.dumps(C1)}")
    # print(f"Encrypted Message: {encrypted_message}")
    # deserialized_point = ECC.Point.from_string(C1)
    # print(f"deserialized_point: {deserialized_point}")
    # print(f"type(deserialized_point): {type(deserialized_point)}")
    # decrypted_message = cipher.process_ecc(encrypted_message, private_key, "decrypt", deserialized_point)
    # print(f"Decrypted Message: {decrypted_message}")


    # print(cipher.process_ca(b"hello world", "0110101", 110, 3, "encrypt"))
    # print(cipher.process_des(b"hello world",b"12345678" ,"encrypt"))
    # print(cipher.process_md5(b"12345678"))
    

