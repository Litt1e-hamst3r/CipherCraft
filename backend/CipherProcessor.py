import sys
import os
import json
import base64

# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from crypto import AES, RSA, ECC, md5, CA, DES, DH, RC4, utils
from crypto.classical import danbiao, duobiao, duotu, zhihuan

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
        key = (key[0], key[1])
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
        try:
            seed = [int(char) for char in seed_str]
            rule = int(rule)
            key_position = int(key_position)
        except: return self.__generate_error(-1, "输入内容应为整数")
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
        try:
            key_size = int(key_size)
        except: return self.__generate_error(-1, "密钥长度必须为整数")
        if key_size > 1025:
            return self.__generate_error(-1, "运算能力有限，密钥长度不能大于1024")
        rsa = RSA.RSA_Cipher(key_size=key_size)
        return rsa.public_key, rsa.private_key

    def process_rsa(self, message, key, mode):
        rsa = RSA.RSA_Cipher()
        if mode == 'encrypt':
            try:
                public_key = int(key['public_key'][0]), int(key['public_key'][1])
            except: return self.__generate_error(-1, "公钥格式错误")
            return rsa.encrypt(message, public_key)
        elif mode == 'decrypt':
            try:
                private_key = int(key['private_key'][0]), int(key['private_key'][1])
            except: return self.__generate_error(-1, "私钥格式错误")
            return rsa.decrypt(message, private_key)

    def process_auto_ecc(self, b):
        try:
            b = int(b)
        except: return self.__generate_error(-1, "参数格式错误, 输入应为整数")
        ecc = ECC.ECC_Cipher(b=b)
        ecc.public_key = str(ecc.public_key)
        return ecc.public_key, ecc.private_key

    def process_ecc(self, message, key, mode):
        ecc = ECC.ECC_Cipher()
        if mode == 'encrypt':
            try:
                key = f'({key['public_key'][0]},{key['public_key'][1]},a=0,p=115792089237316195423570985008687907853269984665640564039457584007908834671663)'
                key = ECC.Point.from_string(key)
            except: return self.__generate_error(-1, "ECC 公钥格式错误")
            c1, encrypted_message = ecc.encrypt(message, key)
            return [str(c1), encrypted_message]
        elif mode == 'decrypt':
            try:
                C1 = f'({key['private_key'][0]},{key['private_key'][1]},a=0,p=115792089237316195423570985008687907853269984665640564039457584007908834671663)'
                C1 = ECC.Point.from_string(C1)
                private_key = int(key['private_key'][2])
            except: return self.__generate_error(-1, "ECC 私钥格式错误")
            return ecc.decrypt(C1, message, private_key)
        
    def process_md5(self, message):
        m = md5.md5_Cipher()
        return m.digest(message)
    
    def process_caesar(self, message, key, mode):
        try:
            key = int(key[0])
            
            if not 0 <= key <= 25: return self.__generate_error(-1, "key 必须为0~25之间的整数")
        except: return self.__generate_error(-1, "key 必须为0~25之间的整数")
        cs = danbiao.Danbiao_Cipher()
        if mode=='encrypt':
            return cs.caesar_cipher(message, key)
        elif mode=='decrypt':
            return cs.caesar_cipher(message, key, decrypt=True)
    
    def process(self):
        
        for json_part in self.json_list:
            key = b""

            # 统一key
            try:
                if json_part['key_type'] == 'Hex':
                    key = bytes.fromhex(json_part['key'][0])
                elif json_part['key_type'] == 'Raw':
                    key = json_part['key'][0].encode()
                else: key = json_part['key']
            except: return self.__generate_error(-1, "key 格式错误")

            # 统一input
            try:
                if json_part['input_type'] == "Hex":
                    self.message = bytes.fromhex(self.message)
                elif json_part['input_type'] == "Raw":
                    self.message = self.message.encode()
            except: return self.__generate_error(-1, "input 格式错误")

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
                if mode == 'encrypt':
                    result[1] = result[1].hex()
                    return result   # 由于是一个 list 列表，所以直接返回
            elif alogorithm == 'MD5 Hashing': 
                result = self.process_md5(self.message.encode())
                return result
            # CA 比较特殊
            elif alogorithm == 'CA': 
                seed_str = key[0]
                rule = key[1]
                key_position = key[2]
                result = self.process_ca(self.message, seed_str, rule, key_position, mode)

            # 传统的加解密算法
                # 单表：
                # 'Caesar',
                # 'Keyword',
                # 'Affine',
                # 'Multiliteral',
            elif alogorithm == 'Caesar':
                result = self.process_caesar(self.message, key, mode)

            # 自动生成密钥就结束
            elif alogorithm == 'Auto RSA Key':
                result = self.process_auto_rsa(key[0])
                return result
            elif alogorithm == 'Auto ECC Key':
                result = self.process_auto_ecc(key[0])
                return result
            
            # 判断 result 是否为 {"error_code": error_code, "error_message": error_message} 格式
            if isinstance(result, dict) and 'error_code' in result and 'error_message' in result:
                return result
            
            # result 是 bytes 类型
            if json_part['output_type'] == 'Hex':
                self.message = result.hex()
            elif json_part['output_type'] == 'Raw':
                try:
                    self.message = result.decode()
                except:
                    return self.__generate_error(-1, "无法转为 Raw, 请尝试 Hex")
            else:
                self.message = result
            # 输出解密结果
        return self.message
            


if __name__ == '__main__':

    message = "Hello, World!"

    # RSA
    # json_list = [{'algorithm': 'RSA', 'key': {'public_key': ['11513131660207132678430883972359855093257615465552668817252751237121474307254261222172914603374915232195641802690837530495058374926950438256454716872803704592660898421945230911417599769684610208339585713782617683338640759700543011625710758181139032044004982168385522631845891541825658477126684217315613134710611080102030283069429925670785908566127455141602517812582850629108473955718879926770093767187379280242899936936957998986993831808095977177884268035555196341884665508927337328127884924274289221048963178534755038655306648806776289344375068680735796971353781525548561681976528882086276192900365915980994314173123', '65537'], 'private_key': ['', '']}, 'mode': 'encrypt', 'key_type': '', 'input_type': 'Raw', 'output_type': 'Hex'}, {'algorithm': 'RSA', 'key': {'public_key': ['', ''], 'private_key': ['11513131660207132678430883972359855093257615465552668817252751237121474307254261222172914603374915232195641802690837530495058374926950438256454716872803704592660898421945230911417599769684610208339585713782617683338640759700543011625710758181139032044004982168385522631845891541825658477126684217315613134710611080102030283069429925670785908566127455141602517812582850629108473955718879926770093767187379280242899936936957998986993831808095977177884268035555196341884665508927337328127884924274289221048963178534755038655306648806776289344375068680735796971353781525548561681976528882086276192900365915980994314173123', '7196475860359570779436366662003470770637933038533425059107968848569223415729600240571180351972983238276003882497370331823703653339068384319936333318498005075581026044142795432903885966173765310963747635154262987289125512628480773780417797715647045908153624586537573197027128904449213414033212062839832339951636448706208784163154588868159977826069050917037577514880399618725572537488260790478873121595406216110310952183690529347498381055664392720864741353836622919919603698422805342735783469349879223934442637446654699370079609408429191072019709575619340551846833393959276401221380202841563171430525286927883712928473']}, 'mode': 'decrypt', 'key_type': '', 'input_type': 'Hex', 'output_type': 'Raw'}]
    
    # Auto RSA Key
    # json_list = [{'algorithm': 'Auto RSA Key', 'key': ['1000'], 'mode': 'encrypt', 'key_type': '', 'input_type': '', 'output_type': ''}]
    
    # Auto ECC Key
    # json_list = [{'algorithm': 'Auto ECC Key', 'key': ['7'], 'mode': 'encrypt', 'key_type': '', 'input_type': '', 'output_type': ''}]
    
    # ECC encrypt
    # json_list = [{'algorithm': 'ECC', 'key': {'public_key': ['72700708536793286189700092802166568116408092341783000567130196869862852866517', '96676952564767445173395068126200898054474725506638262144492283233005224230126'], 'private_key': ['', '']}, 'mode': 'encrypt', 'key_type': '', 'input_type': 'Raw', 'output_type': 'Hex'},]
    # ECC decrypt
    # message = "a7cf0a34f89a832c88456454582fd4e9a99889e86fbb3c31d6ab90a45f648b48"
    # json_list = [{'algorithm': 'ECC', 'key': {'public_key': ['', ''], 'private_key': ['41031872500330896324117368551512841166567919784393892103725375678091008386330', '4172558346003933223247840607826297906270650023398740643420497153666162351469', '50613016897095371335726342381219217750727084709287216287047745755920187282328']}, 'mode': 'decrypt', 'key_type': '', 'input_type': 'Hex', 'output_type': 'Raw'},]
    
    # AES
    # json_list = [{'algorithm': 'AES', 'key': ['1234567890123456'], 'mode': 'encrypt', 'key_type': 'Raw', 'input_type': 'Raw', 'output_type': 'Hex'}, 
    #              {'algorithm': 'AES', 'key': ['1234567890123456'], 'mode': 'decrypt', 'key_type': 'Raw', 'input_type': 'Hex', 'output_type': 'Raw'}]
    
    # DES
    # json_list = [{'algorithm': 'DES', 'key': ['12345678'], 'mode': 'encrypt', 'key_type': 'Raw', 'input_type': 'Raw', 'output_type': 'Hex'}, {'algorithm': 'DES', 'key': ['12345678'], 'mode': 'decrypt', 'key_type': 'Raw', 'input_type': 'Hex', 'output_type': 'Raw'}]
    
    # RC4
    # json_list = [{'algorithm': 'RC4', 'key': ['EQWEQWWEQE'], 'mode': 'encrypt', 'key_type': 'Raw', 'input_type': 'Hex', 'output_type': 'Hex'}, {'algorithm': 'RC4', 'key': ['EQWEQWWEQE'], 'mode': 'decrypt', 'key_type': 'Raw', 'input_type': 'Hex', 'output_type': 'Raw'}]
    
    # CA
    # message = message.encode().hex()
    # json_list =  [{'algorithm': 'CA', 'key': ['010101010101011', '100', '3'], 'mode': 'encrypt', 'key_type': '', 'input_type': 'Hex', 'output_type': 'Hex'}, {'algorithm': 'CA', 'key': ['010101010101011', '100', '3'], 'mode': 'decrypt', 'key_type': '', 'input_type': 'Hex', 'output_type': 'Raw'}]
    
    # MD5
    # json_list =  [{'algorithm': 'MD5 Hashing', 'key': '', 'mode': '', 'key_type': '', 'input_type': '', 'output_type': ''}]

    # Caesar
    # json_list = [{'algorithm': 'Caesar', 'key': ['12'], 'mode': 'encrypt', 'key_type': '', 'input_type': 'Raw', 'output_type': 'Raw'}, {'algorithm': 'Caesar', 'key': ['12'], 'mode': 'decrypt', 'key_type': '', 'input_type': 'Raw', 'output_type': 'Raw'}]

    print(f"message: {message}")
    cipher_processor = CipherProcessor(message, json_list)
    encrypted_message = cipher_processor.process()
    print(f"Encrypted Message: {encrypted_message}")
    
    # ECC
    # cipher = CipherProcessor("", "")
    # public_key, private_key = cipher.process_auto_ecc(7)
    # print(f"Private Key: {private_key}")
    # print(f"Public Key: {public_key}")
    # public_key = ECC.Point.from_string(public_key)
    # json_list = [{'algorithm': 'ECC', 'key': {'public_key': [str(public_key.x), (str(public_key.y))], 'private_key': ['', '']}, 'mode': 'encrypt', 'key_type': '', 'input_type': 'Raw', 'output_type': 'Hex'},]
    # print(json_list)
    # a = cipher.process_ecc(message.encode(), {'public_key': [str(public_key.x), (str(public_key.y))]}, "encrypt")
    # print(f"a: {a}")
    # C1, encrypted_message = a[0], a[1]
    # print(f"C1: {C1}")
    # print(f"Encrypted Message: {encrypted_message}")
    # deserialized_point = ECC.Point.from_string(C1)
    # print(f"deserialized_point: {deserialized_point}")
    # print(f"type(deserialized_point): {type(deserialized_point)}")
    # decrypted_message = cipher.process_ecc(encrypted_message, {'private_key': [deserialized_point.x, deserialized_point.y, private_key]}, "decrypt")
    # print(f"Decrypted Message: {decrypted_message}")


    # print(cipher.process_ca(b"hello world", "0110101", 110, 3, "encrypt"))
    # print(cipher.process_des(b"hello world",b"12345678" ,"encrypt"))
    # print(cipher.process_md5(b"12345678"))
    

