

class Duobiao_Cipher:
    def __init__(self):
        pass  # 初始化可以保持为空

    def vigenere_cipher(self, text, key, decrypt=False):
        result = bytearray()
        text_bytes = text  # 输入已经是字节
        key_bytes = key.upper()  # 密钥统一为大写
        key_length = len(key_bytes)

        for i, char in enumerate(text_bytes):
            if 65 <= char <= 90 or 97 <= char <= 122:  # 处理 A-Z 和 a-z
                is_upper = 65 <= char <= 90  # 判断当前字符是否为大写
                base = 65 if is_upper else 97  # 根据大小写选择基准值

                shift = key_bytes[i % key_length] - 65  # 假设密钥是大写字母 A-Z
                if decrypt:
                    shift = -shift  # 解密时反向移动
                index = (char - base + shift) % 26  # 26 是字母表的长度
                decrypted_char = base + index  # 将结果转换回相应的字母
                result.append(decrypted_char)
            else:
                result.append(char)  # 非字母字符直接添加到结果中

        return result  # 返回字节数组

    def autokey_cipher_ciphertext(self, text, key, decrypt=False):
        result = bytearray()
        text_bytes = text  # 输入已经是字节
        extended_key = key.upper()  # 密钥统一为大写

        for i, char in enumerate(text_bytes):
            if 65 <= char <= 90 or 97 <= char <= 122:  # 处理 A-Z 和 a-z
                is_upper = 65 <= char <= 90  # 判断当前字符是否为大写
                base = 65 if is_upper else 97  # 根据大小写选择基准值

                if i >= len(extended_key):
                    if not decrypt:
                        # 在加密时，使用已生成的密文字符来扩展密钥
                        extended_key += bytes([text_bytes[i]])
                    elif decrypt and result:
                        # 在解密时，使用已解密的最后一个字符来扩展密钥
                        extended_key += bytes([result[-1]])

                shift = extended_key[i] - 65  # 假设密钥是大写字母 A-Z
                if decrypt:
                    shift = -shift  # 解密时反向移动
                index = (char - base + shift) % 26  # 26 是字母表的长度
                decrypted_char = base + index  # 将结果转换回相应的字母
                result.append(decrypted_char)

                # 更新密钥
                if not decrypt:
                    extended_key += bytes([text_bytes[i]])  # 加密时使用当前字符更新密钥
                else:
                    extended_key += bytes([decrypted_char])  # 解密时使用新解密的明文字符更新密钥
            else:
                result.append(char)  # 非字母字符直接添加到结果中

        return result  # 返回字节数组

    def autokey_cipher_plaintext(self, text, key, decrypt=False):
        result = bytearray()
        text_bytes = text  # 输入已经是字节
        extended_key = key.upper()  # 密钥统一为大写

        for i, char in enumerate(text_bytes):
            if 65 <= char <= 90 or 97 <= char <= 122:  # 处理 A-Z 和 a-z
                is_upper = 65 <= char <= 90  # 判断当前字符是否为大写
                base = 65 if is_upper else 97  # 根据大小写选择基准值

                if i >= len(extended_key):
                    if decrypt and result:  # 确保 result 不为空
                        # 在解密时，使用已解密的最后一个字符来扩展密钥
                        extended_key += bytes([result[-1]])

                shift = extended_key[i] - 65  # 假设密钥是大写字母 A-Z
                if decrypt:
                    shift = -shift  # 解密时反向移动
                index = (char - base + shift) % 26  # 26 是字母表的长度
                decrypted_char = base + index  # 将结果转换回相应的字母
                result.append(decrypted_char)

                if not decrypt and i >= len(extended_key) - 1:
                    # 在加密时，使用原文中的字符来扩展密钥
                    extended_key += bytes([text_bytes[i]])
            else:
                result.append(char)  # 非字母字符直接添加到结果中

        return result  # 返回字节数组

if __name__ == "__main__":
    cipher = Duobiao_Cipher()

    while True:
        print("\n选择加密方式:")
        print("1. Vigenere Cipher")
        print("2. Autokey Cipher (Ciphertext)")
        print("3. Autokey Cipher (Plaintext)")
        print("4. 退出")

        choice = input("输入选项 (1-4): ")
        if choice == '4':
            print("已退出.")
            break

        if choice not in ['1', '2', '3']:
            print("无效选项，请重新输入 (1-4).")
            continue

        key = input("输入密钥 (string): ").encode('ascii')  # 密钥可以是任意字符串，但我们会将其转换为大写

        # Loop for encryption/decryption operations with the same key
        while True:
            action = input("选择加密e/解密d/返回上一级r? (e/d/r): ").strip().lower()
            if action not in ['e', 'd', 'r']:
                print("无效选项，输入e(加密)/d(解密)/r(返回上一级).")
                continue
            if action == 'r':
                break  # Return to choose encryption method

            text = input("输入文本: ").encode('ascii')  # 输入文本转换为字节

            if choice == '1':
                if action == 'e':
                    encrypted_text = cipher.vigenere_cipher(text, key)
                elif action == 'd':
                    encrypted_text = cipher.vigenere_cipher(text, key, decrypt=True)
            elif choice == '2':
                if action == 'e':
                    encrypted_text = cipher.autokey_cipher_ciphertext(text, key)
                elif action == 'd':
                    encrypted_text = cipher.autokey_cipher_ciphertext(text, key, decrypt=True)
            elif choice == '3':
                if action == 'e':
                    encrypted_text = cipher.autokey_cipher_plaintext(text, key)
                elif action == 'd':
                    encrypted_text = cipher.autokey_cipher_plaintext(text, key, decrypt=True)

            # 打印结果时，将字节数组转换为字符串
            print(f"结果: {encrypted_text.decode('ascii')}")  # 显示结果