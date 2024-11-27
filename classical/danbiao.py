import string

class Danbiao_Cipher:
    def __init__(self):
        pass  # 初始化方法可以保持为空

    def caesar_cipher(self, text, shift, decrypt=False):
        result = b""
        for char in text:
            if 65 <= char <= 90:  # A-Z
                shifted = (char - 65 + (-shift if decrypt else shift)) % 26 + 65
                result += bytes([shifted])
            elif 97 <= char <= 122:  # a-z
                shifted = (char - 97 + (-shift if decrypt else shift)) % 26 + 97
                result += bytes([shifted])
            else:
                result += bytes([char])
        return result

    def keyword_cipher(self, text, keyword, decrypt=False):
        # 确保text和keyword都是字节串
        if not isinstance(text, bytes) or not isinstance(keyword, bytes):
            raise TypeError("both_text_and_keyword_must_be_bytes")

        # 将keyword转换为大写并移除重复字符，同时保持原始顺序
        unique_keyword = ''.join(dict.fromkeys(keyword.decode('utf-8').upper()))
        alphabet_upper = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
        remaining_letters_upper = ''.join([c for c in alphabet_upper if c not in unique_keyword])
        key_alphabet_upper = list(unique_keyword + remaining_letters_upper)

        # 为小写字母创建对应的密钥字母表
        alphabet_lower = [chr(c) for c in range(ord('a'), ord('z') + 1)]
        key_alphabet_lower = [c.lower() for c in key_alphabet_upper]

        result = b""
        for char in text:
            if 65 <= char <= 90:  # A-Z
                original_char = chr(char)
                if not decrypt:
                    index = key_alphabet_upper.index(original_char)
                    encrypted_char = alphabet_upper[index]
                else:
                    index = alphabet_upper.index(original_char)
                    encrypted_char = key_alphabet_upper[index]
            elif 97 <= char <= 122:  # a-z
                original_char = chr(char)
                if not decrypt:
                    index = key_alphabet_lower.index(original_char)
                    encrypted_char = alphabet_lower[index]
                else:
                    index = alphabet_lower.index(original_char)
                    encrypted_char = key_alphabet_lower[index]
            else:
                result += bytes([char])
                continue

            result += bytes([ord(encrypted_char)])

        return result

    def affine_cipher(self, text, a, b, decrypt=False):
        if self.__gcd(a, 26) != 1:
            raise ValueError("a_and_26_must_be_coprime")

        result = b""
        for char in text:
            if 65 <= char <= 90:  # A-Z
                base = 65
            elif 97 <= char <= 122:  # a-z
                base = 97
            else:
                result += bytes([char])
                continue

            if decrypt:
                index = (self.__mod_inverse(a, 26) * ((char - base) - b)) % 26
            else:
                index = (a * (char - base) + b) % 26

            result += bytes([index + base])

        return result

    def multiliteral_cipher(self, text, key, decrypt=False):
        key_length = len(key)
        result = b""

        for i, char in enumerate(text):
            if 65 <= char <= 90:  # A-Z
                base = 65
            elif 97 <= char <= 122:  # a-z
                base = 97
            else:
                result += bytes([char])
                continue

            # 将key中的字节转换为字符
            key_char = chr(key[i % key_length])
            shift = ord(key_char.upper()) - 65
            if decrypt:
                shift = -shift

            index = (char - base + shift) % 26 + base
            result += bytes([index])

        return result

    def __gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def __mod_inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1


# 主程序
if __name__ == "__main__":
    cipher = Danbiao_Cipher()

    while True:
        print("\n请选择加密方式:")
        print("1. Caesar Cipher")
        print("2. Keyword Cipher")
        print("3. Affine Cipher")
        print("4. Multiliteral Cipher")
        print("5. 退出")

        choice = input("输入选项 (1-5): ")
        if choice == '5':
            print("已退出.")
            break

        action = input("请选择操作（加密e/解密d/返回上一级r）: ").strip().lower()
        if action not in ['e', 'd', 'r']:
            print("无效操作，请输入 e, d 或 r.")
            continue
        if action == 'r':
            continue  # 返回上一级菜单

        text = input("输入文本: ").encode('utf-8')  # 将输入文本转换为字节串

        try:
            if choice == '1':
                shift = int(input("输入偏移值: "))
                encrypted_text = cipher.caesar_cipher(text, shift, decrypt=(action == 'd'))
            elif choice == '2':
                keyword = input("输入密钥: ").encode('utf-8')  # 将关键词转换为字节串
                encrypted_text = cipher.keyword_cipher(text, keyword, decrypt=(action == 'd'))
            elif choice == '3':
                a = int(input("输入a值: "))
                b = int(input("输入b值: "))
                encrypted_text = cipher.affine_cipher(text, a, b, decrypt=(action == 'd'))
            elif choice == '4':
                key = input("输入密钥(string): ").encode('utf-8')  # 将密钥转换为字节串
                encrypted_text = cipher.multiliteral_cipher(text, key, decrypt=(action == 'd'))
            else:
                print("无效选项")
                continue
        except Exception as e:
            print(f"发生错误: {e}")
            continue

        # 输出时解码为字符串以便于阅读
        print(f"结果: {encrypted_text.decode('utf-8')}")
