import random
import cryptography

# Define sbox as a global variable
sbox = bytes(range(256))

def generate_key(length):
    return bytes(random.randint(0, 255) for _ in range(length))

def apply_sbox(plaintext):
    # Use the global sbox variable
    return bytes(sbox[b] for b in plaintext)

def apply_permutation(plaintext, permutation):
    return bytes((plaintext[i // 8] >> (i % 8)) & 1 for i in permutation)

def encrypt(plaintext):
    key = generate_key(len(plaintext))
    key_whitened_plaintext = bytes(a ^ b for a, b in zip(plaintext, key))
    key_portion_1 = key_whitened_plaintext[:len(key_whitened_plaintext) // 2]
    key_portion_2 = key_whitened_plaintext[len(key_whitened_plaintext) // 2:]
    round_keys = []
    for i in range(10):
        # Pass sbox as an argument
        round_key = apply_sbox(key_portion_1)
        round_keys.append(round_key)
        key_portion_1 = bytes(a ^ b for a, b in zip(key_portion_1, round_key))
    ciphertext = key_whitened_plaintext
    for i in range(10):
        sbox_output = apply_sbox(ciphertext)
        permutation_output = apply_permutation(sbox_output, range(len(ciphertext) * 8))
        ciphertext = bytes(a ^ b for a, b in zip(permutation_output, round_keys[i]))
    ciphertext = bytes(a ^ b for a, b in zip(ciphertext, key_portion_2))
    return ciphertext

plaintext = b"Hello, world!"
ciphertext = encrypt(plaintext)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)

# Plaintext: b'Hello, world!'
# Ciphertext: b'f.=\xd0^<'
