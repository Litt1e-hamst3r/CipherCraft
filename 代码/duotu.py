class Playfair_Cipher:
    def __init__(self):
        pass  # 初始化可以保持为空

    def __generate_table(self, key):
        key = key.upper().replace(b'J', b'I')
        # 使用 bytearray 来处理排序和去重
        key = bytearray(sorted(set(key), key=key.find))
        alphabet = b'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        table = key + bytearray(sorted(set(alphabet) - set(key)))
        return [table[i:i + 5] for i in range(0, 25, 5)]

    def __prepare_text(self, text):
        text = text.upper().replace(b'J', b'I').replace(b' ', b'')
        i = 0
        while i < len(text) - 1:
            if text[i] == text[i + 1]:
                text = text[:i + 1] + b'X' + text[i + 1:]
            i += 2
        if len(text) % 2 != 0:
            text += b'X'
        return text

    def __find_position(self, table, char):
        for i in range(5):
            for j in range(5):
                if table[i][j] == char:
                    return i, j
        raise ValueError(f"Character '{char}' not found in the table.")

    def __encrypt_pair(self, table, a, b):
        try:
            row_a, col_a = self.__find_position(table, a)
            row_b, col_b = self.__find_position(table, b)
        except ValueError as e:
            print(e)
            return b''

        if row_a == row_b:
            return table[row_a][(col_a + 1) % 5].to_bytes(1, 'big') + table[row_b][(col_b + 1) % 5].to_bytes(1, 'big')
        elif col_a == col_b:
            return table[(row_a + 1) % 5][col_a].to_bytes(1, 'big') + table[(row_b + 1) % 5][col_b].to_bytes(1, 'big')
        else:
            return table[row_a][col_b].to_bytes(1, 'big') + table[row_b][col_a].to_bytes(1, 'big')

    def encrypt(self, text, key):
        table = self.__generate_table(key)
        text = self.__prepare_text(text)
        ciphertext = b''
        for i in range(0, len(text), 2):
            ciphertext += self.__encrypt_pair(table, text[i], text[i + 1])
        return ciphertext  # 返回 bytes 类型

    def __decrypt_pair(self, table, a, b):
        try:
            row_a, col_a = self.__find_position(table, a)
            row_b, col_b = self.__find_position(table, b)
        except ValueError as e:
            print(e)
            return b''

        if row_a == row_b:
            return table[row_a][(col_a - 1) % 5].to_bytes(1, 'big') + table[row_b][(col_b - 1) % 5].to_bytes(1, 'big')
        elif col_a == col_b:
            return table[(row_a - 1) % 5][col_a].to_bytes(1, 'big') + table[(row_b - 1) % 5][col_b].to_bytes(1, 'big')
        else:
            return table[row_a][col_b].to_bytes(1, 'big') + table[row_b][col_a].to_bytes(1, 'big')

    def decrypt(self, ciphertext, key):
        table = self.__generate_table(key)
        plaintext = b''
        for i in range(0, len(ciphertext), 2):
            plaintext += self.__decrypt_pair(table, ciphertext[i], ciphertext[i + 1])
        return plaintext.replace(b'X', b'')  # 返回 bytes 类型


if __name__ == "__main__":
    playfair_cipher = Playfair_Cipher()

    while True:
        print("\nPlayfair Cipher")
        print("1. 加密")
        print("2. 解密")
        print("3. 退出")
        choice = input("请选择一个选项 (1/2/3): ")

        if choice == '1':
            key = input("请输入密钥: ").upper().encode('ascii')
            plaintext = input("请输入明文: ").upper().encode('ascii')
            ciphertext = playfair_cipher.encrypt(plaintext, key)
            print(f"加密后的密文: {ciphertext.decode('ascii')}")  # 显示为字符串
        elif choice == '2':
            key = input("请输入密钥: ").upper().encode('ascii')
            ciphertext = input("请输入密文: ").upper().encode('ascii')
            plaintext = playfair_cipher.decrypt(ciphertext, key)
            print(f"解密后的明文: {plaintext.decode('ascii')}")  # 显示为字符串
        elif choice == '3':
            print("退出程序。")
            break
        else:
            print("无效的选择，请重新输入。")