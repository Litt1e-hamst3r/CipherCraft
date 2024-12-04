import string
import random
from math import gcd

def get_caesar_key(seed):
    return [str(seed % 26 + 1)]

def get_keyword_key(seed, length=10):
    random.seed(seed)
    keyword = ''.join(random.choices(string.ascii_lowercase, k=length))
    return [keyword]

def get_affine_keys(seed):
    b = seed % 26
    a = (seed // 26) % 26
    while gcd(a, 26) != 1:
        a = (a + 1) % 26
        if a == 0:
            a += 1
    return [str(a), str(b)]

def get_multiliteral_key(seed, alphabet_size=26, key_length=10):
    random.seed(seed)
    return [''.join(random.choices(string.ascii_uppercase[:alphabet_size], k=key_length))]

def get_vigenere_key(seed, length=10):
    random.seed(seed)
    return [''.join(random.choices(string.ascii_uppercase, k=length))]

def get_autokey_ciphertext_key(seed, length=10):
    random.seed(seed)
    return [''.join(random.choices(string.ascii_uppercase, k=length))]

def get_autokey_plaintext_key(seed, length=10):
    random.seed(seed)
    return [''.join(random.choices(string.ascii_uppercase, k=length))]

def get_playfair_key(seed):
    keyword = get_keyword_key(seed)[0]
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    playfair_matrix = []
    used_letters = set()

    for char in keyword:
        if char not in used_letters and char != 'J':
            playfair_matrix.append(char)
            used_letters.add(char)

    for char in alphabet:
        if char not in used_letters:
            playfair_matrix.append(char)

    return [''.join(playfair_matrix)]

def get_permutation_key(seed, length=26):
    random.seed(seed)
    letters = list(string.ascii_uppercase[:length])
    random.shuffle(letters)
    return [''.join(letters)]

def get_column_permutation_key(seed, num_columns=5):
    random.seed(seed)
    column_permutation = ''.join(map(str, random.sample(range(num_columns), num_columns)))
    return [column_permutation]  # 将列排列转换为单个字符串

def get_double_transposition_key(seed, num_rows=5, num_columns=5):
    random.seed(seed)
    row_permutation = get_column_permutation_key(seed, num_rows)[0]
    column_permutation = get_column_permutation_key(seed, num_columns)[0]
    return [row_permutation, column_permutation]  # 将行和列的排列分别作为两个字符串


def get_rc4_key(seed_str, length=8):
    if len(seed_str) < length:
        seed_str = (seed_str * (length // len(seed_str) + 1))[:length]
    selected_digits = random.sample(seed_str, length)
    key = ''.join(selected_digits)
    return [key]

def get_des_key(seed_str):
    if len(seed_str) < 8:
        seed_str = (seed_str * (8 // len(seed_str) + 1))[:8]
    selected_digits = random.sample(seed_str, 8)
    key = ''.join(selected_digits)
    return [key]

def get_aes_key(seed_str, key_size=16):
    if len(seed_str) < key_size:
        seed_str = (seed_str * (key_size // len(seed_str) + 1))[:key_size]
    selected_digits = random.sample(seed_str, key_size)
    key = ''.join(selected_digits)
    return [key]

def get_ca_key(seed):
    random.seed(seed)
    initial_state = random.randint(0, 255)
    binary_initial_state = format(initial_state, '08b')
    key_position = random.randint(0, len(binary_initial_state) - 1)
    rule_number = random.randint(0, 255)
    return [binary_initial_state, str(rule_number), str(key_position)]

def get_key_from_integer(integer_seed, algorithm):
    # 将整数转换为字符串
    seed_str = str(integer_seed)
    random.seed(integer_seed)

    if algorithm == 'Caesar':
        return get_caesar_key(integer_seed)
    elif algorithm == 'Keyword':
        return get_keyword_key(integer_seed)
    elif algorithm == 'Affine':
        return get_affine_keys(integer_seed)
    elif algorithm == 'Multiliteral':
        return get_multiliteral_key(integer_seed)
    elif algorithm == 'Vigenere':
        return get_vigenere_key(integer_seed)
    elif algorithm == 'Autokey Ciphertext':
        return get_autokey_ciphertext_key(integer_seed)
    elif algorithm == 'Autokey Plaintext':
        return get_autokey_plaintext_key(integer_seed)
    elif algorithm == 'Playfair':
        return get_playfair_key(integer_seed)
    elif algorithm == 'Permutation':
        return get_permutation_key(integer_seed)
    elif algorithm == 'Column permutation':
        return get_column_permutation_key(integer_seed)
    elif algorithm == 'Double-Transposition':
        return get_double_transposition_key(integer_seed)
    elif algorithm == 'RC4':
        return get_rc4_key(seed_str)
    elif algorithm == 'CA':
        return get_ca_key(integer_seed)
    elif algorithm == 'DES':
        return get_des_key(seed_str)
    elif algorithm == 'AES':
        return get_aes_key(seed_str)
    elif algorithm == 'Autokey ciphertext' or algorithm == 'Autokey plaintext':
        return get_vigenere_key(seed_str)
    else:
        raise ValueError("Unsupported algorithm")

if __name__ == '__main__':
    # 例子
    integer_seed = 129341839790198209880448170773785713142599103022634936945934775490901565370690145092810994072869272349792364594170465485168315524876607395803070975007552090519808993311890345121233469388263452500815923392139119422050690606530221676547867276153629134283662439431229879164876057454261034359432043538478800425695
    algorithms = [
        'Autokey Ciphertext', 'Autokey Plaintext', 'Playfair', 'Permutation','Caesar',
        'Column permutation', 'Double-Transposition', 'RC4', 'CA', 'DES', 'AES'
    ]

    for algo in algorithms:
        key = get_key_from_integer(integer_seed, algo)
        print(f"{algo} Key: {key}")