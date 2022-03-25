def int_to_bytes(val: int) -> bytes:
    return val.to_bytes((val.bit_length() + 7) // 8, 'big')

# super duper simple encryption via XOR. not so secure!
def encrypt(msg: str, key: int):
    key_bytes = int_to_bytes(key)
    enc_bytes = xor_bytes(msg.encode('utf-8'), key_bytes)
    return enc_bytes

def decrypt(msg: bytes, key: int) -> bytes:
    key_bytes = int_to_bytes(key)
    decrypted_bytes = xor_bytes(msg, key_bytes)
    return decrypted_bytes

def xor_bytes(b1: bytes, b2: bytes):
    parts = []
    extended_b2 = b2 * int(len(b1) / len(b2) + 1)
    for b1, b2 in zip(b1, extended_b2):
        parts.append(bytes([b1 ^ b2]))
    return b''.join(parts)
