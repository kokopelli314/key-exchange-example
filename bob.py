from multiprocessing.connection import Client
from random import randrange

from encryptionlib import encrypt, int_to_bytes

public_modulus_p = 23122312231223122312
public_base_g = 5

bob_secret = randrange(1, 10)
bob_public = (public_base_g ** bob_secret) % public_modulus_p
encryption_key = None # To be determined in handshake

def begin(port):
    conn = Client(('localhost', port))
    print('Bob connected to port', port)

    print('\nBob\'s secret:', bob_secret)
    print('--- Decimal:\t' + str(bob_secret))
    print('--- Bytes:\t' + str(int_to_bytes(bob_secret)))

    conn.send('public:' + str(bob_public))
    response = conn.recv()
    alice_public_key = int(response.split('public:')[1])
    print('\nBob received Alice\'s public key:', alice_public_key)

    encryption_key = (alice_public_key ** bob_secret) % public_modulus_p
    print('\bBob generated secret key:')
    print('--- Decimal:\t' + str(encryption_key))
    print('--- Bytes:\t' + str(int_to_bytes(encryption_key)))

    while True:
        input_text = input('> ')
        conn.send(encrypt(input_text, encryption_key))
        if input_text == 'close':
            break

    conn.close()

if __name__ == '__main__':
    begin(4000)

