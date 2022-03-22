import sys

# super duper simple encryption via XOR. not so secure!
def encrypt(msg: str, key: int):
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
    enc_bytes = xor_bytes(msg.encode('utf-8'), key_bytes)
    return enc_bytes
    # repeat key til length of message
    # extended_key = key.to_bytes * int(num.bit_length() / key.bit_length())
    # print(bin(extended_key))
    # return num ^ extended_key

def decrypt(msg: bytes, key: int) -> bytes:
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
    decrypted_bytes = xor_bytes(msg, key_bytes)
    return decrypted_bytes
    # convert decrypted number back to unicode
    # decrypted_bytes = decrypted_num.to_bytes(
    #     (decrypted_num.bit_length() + 7) // 8,
    #     'big',
    # )
    # return decrypted_bytes

def xor_bytes(b1: bytes, b2: bytes):
    parts = []
    extended_b2 = b2 * int(len(b1) / len(b2))
    for b1, b2 in zip(b1, extended_b2):
        parts.append(bytes([b1 ^ b2]))
    return b''.join(parts)
