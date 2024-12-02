import string

class Zhihuan_Cipher:
    def __init__(self):
        pass  # 初始化可以保持为空

    def __generate_permutation_table(self, key):
        key = key.upper()
        indices = list(range(len(key)))
        sorted_key = sorted((char, i) for i, char in enumerate(key))
        permutation_table = [sorted_key.index((key[i], i)) for i in indices]
        return permutation_table

    def __prepare_text(self, text):
        return text.replace(b' ', b'')

    def __pad_text(self, text, block_size):
        padding_length = block_size - (len(text) % block_size)
        if padding_length == block_size:
            padding_length = 0
        padding_char = b'X' if text.isupper() else b'x'
        return text + padding_char * padding_length, padding_length

    def __pad_permute_text(self, text, block_size):
        padding_length = block_size - (len(text) % block_size)
        if padding_length == block_size:
            padding_length = 0
        padding_char = b' ' if text.isupper() else b' '
        return text + padding_char * padding_length

    def __unpad_text(self, text, original_length):
        return text[:original_length]

    def __unpad_permute_text(self, text):
        return text.rstrip(b' ')

    def __permute_block(self, block, permutation_table):
        # 确保block中的每个元素都是字节类型
        block = [bytes([b]) if isinstance(b, int) else b for b in block]
        permuted_block = [b''] * len(block)
        for i in range(len(block)):
            permuted_block[permutation_table[i]] = block[i]
        return b''.join(permuted_block)

    def __permute(self, text, permutation_table, block_size):
        permuted_text = b''
        for i in range(0, len(text), block_size):
            block = text[i:i + block_size]
            permuted_text += self.__permute_block(block, permutation_table)
        return permuted_text

    def __inverse_permutation_table(self, permutation_table):
        inverse_table = [0] * len(permutation_table)
        for i, j in enumerate(permutation_table):
            inverse_table[j] = i
        return inverse_table

    def encrypt_permutation(self, text, key):
        permutation_table = self.__generate_permutation_table(key.decode('ascii'))
        text = self.__prepare_text(text)
        block_size = len(key)
        padded_text = self.__pad_permute_text(text, block_size)
        return self.__permute(padded_text, permutation_table, block_size)

    def decrypt_permutation(self, ciphertext, key):
        permutation_table = self.__generate_permutation_table(key.decode('ascii'))
        inverse_table = self.__inverse_permutation_table(permutation_table)
        block_size = len(key)
        decrypted_text = self.__permute(ciphertext, inverse_table, block_size)
        return self.__unpad_permute_text(decrypted_text)

    def __check(self, t):
        for char in t:
            if char not in string.ascii_letters.encode('ascii'):
                print("错误！请重新输入！")
                return 1
        return 0

    def __transpose(self, text, key, block_size, reverse=False):
        blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]
        transposed_matrix = [[b''] * block_size for _ in range(len(blocks))]
        for i, block in enumerate(blocks):
            for j, char in enumerate(block):
                transposed_matrix[i][j] = bytes([char])  # 确保每个元素都是字节
        permutation_table = self.__generate_permutation_table(key.decode('ascii'))
        if reverse:
            inverse_table = [0] * len(permutation_table)
            for i, col in enumerate(permutation_table):
                inverse_table[col] = i
            permutation_table = inverse_table
        transposed_text = b''
        for row in transposed_matrix:
            for col in range(block_size):
                transposed_text += row[permutation_table[col]]
        return transposed_text

    def double_transpose_encrypt(self, plaintext, key1, key2):
        block_size1 = len(key1)
        padded_text1, _ = self.__pad_text(plaintext, block_size1)
        first_transposed_text = self.__transpose(padded_text1, key1, block_size1, reverse=False)
        block_size2 = len(key2)
        padded_text2, _ = self.__pad_text(first_transposed_text, block_size2)
        second_transposed_text = self.__transpose(padded_text2, key2, block_size2, reverse=False)
        return second_transposed_text

    def double_transpose_decrypt(self, ciphertext, key1, key2):
        block_size2 = len(key2)
        first_decrypted_text = self.__transpose(ciphertext, key2, block_size2, reverse=True)
        block_size1 = len(key1)
        second_decrypted_text = self.__transpose(first_decrypted_text, key1, block_size1, reverse=True)
        decrypted_text = second_decrypted_text.rstrip(b'X').rstrip(b'x')
        return decrypted_text

    def __wordkey(self, key):
        sorted_key = sorted((char, i) for i, char in enumerate(key))
        permutation_table = [0] * len(key)
        for i, (_, original_index) in enumerate(sorted_key):
            permutation_table[original_index] = i + 1
        return permutation_table

    def column_permutation_encrypt(self, plaintext, key):
        # 补“x”或“X”
        t = len(plaintext)
        if t % len(key) != 0:
            padding_length = (len(key) - (t % len(key))) % len(key)
            padding_char = b'X' if plaintext.isupper() else b'x'
            plaintext += padding_char * padding_length

        # 打印矩阵
        n = len(plaintext) // len(key)
        cipher = [[b''] * len(key) for _ in range(n)]
        m = 0
        for i in range(n):
            for j in range(len(key)):
                cipher[i][j] = bytes([plaintext[m]])  # 确保每个元素都是字节
                m += 1

        p = self.__wordkey(key)
        # 加密
        ciphertext = b""
        for i in range(len(key)):
            for j in range(n):
                ciphertext += cipher[j][p[i] - 1]
        return ciphertext

    def column_permutation_decrypt(self, ciphertext, key):
        # 判断是否符合要求
        if len(ciphertext) % len(key) != 0:
            print("\n错误！请重新输入！\n")
            return b""

        p = self.__wordkey(key)

        # 组建明文序列
        n = len(ciphertext) // len(key)
        plain = [[b''] * len(key) for _ in range(n)]
        m = 0
        for i in range(len(key)):
            for j in range(n):
                plain[j][p[i] - 1] = bytes([ciphertext[m]])  # 确保每个元素都是字节
                m += 1

        # 输出明文
        decrypted_text = b""
        for i in range(n):
            for j in range(len(key)):
                decrypted_text += plain[i][j]

        # 去掉填充字符 'X' 或 'x'
        decrypted_text = decrypted_text.rstrip(b'X').rstrip(b'x')
        return decrypted_text


# Main loop
if __name__ == "__main__":
    cipher_suite = Zhihuan_Cipher()

    while True:
        print("\n请选择加密方式：")
        print("1. Permutation cipher")
        print("2. Column permutation cipher")
        print("3. Double-Transposition cipher")
        print("4. 退出")
        choice = input("请输入选项（1/2/3/4）: ")

        if choice == '1':
            key = input("请输入密钥: ").upper().encode('ascii')
            while True:
                action = input("请选择操作（加密1/解密2/返回上一级3）: ")
                if action.lower() == '1':
                    plaintext = input("请输入明文: ").encode('ascii')
                    ciphertext= cipher_suite.encrypt_permutation(plaintext, key)
                    print(f"加密后的密文: {ciphertext.decode('ascii')}")
                elif action.lower() == '2':
                    ciphertext = input("请输入密文: ").encode('ascii')
                    plaintext = cipher_suite.decrypt_permutation(ciphertext, key)
                    print(f"解密后的明文: {plaintext.decode('ascii')}")
                elif action.lower() == '3':
                    break
                else:
                    print("未知的操作，请重新选择。")

        elif choice == '3':
            key1 = input("请输入第一个密钥: ").upper().encode('ascii')
            key2 = input("请输入第二个密钥: ").upper().encode('ascii')
            while True:
                action = input("请选择操作（加密1/解密2/返回上一级3）: ")
                if action.lower() == '1':
                    plaintext = input("请输入明文: ").encode('ascii')
                    ciphertext = cipher_suite.double_transpose_encrypt(plaintext, key1, key2)
                    print(f"加密后的密文: {ciphertext.decode('ascii')}")
                elif action.lower() == '2':
                    ciphertext = input("请输入密文: ").encode('ascii')
                    plaintext = cipher_suite.double_transpose_decrypt(ciphertext, key1, key2)
                    print(f"解密后的明文: {plaintext.decode('ascii')}")
                elif action.lower() == '3':
                    break
                else:
                    print("未知的操作，请重新选择。")

        elif choice == '2':
            key = input("请输入密钥: ").upper().encode('ascii')
            while True:
                action = input("请选择操作（加密1/解密2/返回上一级3）: ")
                if action.lower() == '1':
                    plaintext = input("请输入明文: ").encode('ascii')
                    ciphertext = cipher_suite.column_permutation_encrypt(plaintext, key)
                    print(f"加密后的密文: {ciphertext.decode('ascii')}")
                elif action.lower() == '2':
                    ciphertext = input("请输入密文: ").encode('ascii')
                    plaintext = cipher_suite.column_permutation_decrypt(ciphertext, key)
                    print(f"解密后的明文: {plaintext.decode('ascii')}")
                elif action.lower() == '3':
                    break
                else:
                    print("未知的操作，请重新选择。")

        elif choice == '4':
            break
        else:
            print("无效的选项，请重新选择。")