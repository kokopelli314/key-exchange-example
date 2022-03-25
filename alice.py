from multiprocessing.connection import Listener
from random import randrange

from encryptionlib import decrypt, int_to_bytes


# public variables
public_modulus_p = 23122312231223122312
public_base_g = 5

alice_secret = randrange(1, 10)
alice_public = (public_base_g ** alice_secret) % public_modulus_p
encryption_key = None # To be determined in handshake

def listen(port):
    listener = Listener(('localhost', port))
    print('Alice listening at port', port)

    print('\nAlice\'s secret:', alice_secret)
    print('--- Decimal:\t' + str(alice_secret))
    print('--- Bytes:\t' + str(int_to_bytes(alice_secret)))

    conn = listener.accept()

    while True:
        msg = conn.recv()
        if str(msg).startswith('public:'):
            bob_public_key = int(msg.split('public:')[1])
            print('\nAlice received Bob\'s public key:', bob_public_key)
            conn.send('public:' + str(alice_public))

            encryption_key: int = (bob_public_key ** alice_secret) % public_modulus_p
            print('\nAlice generated secret key:')
            print('--- Decimal:\t' + str(encryption_key))
            print('--- Bytes:\t' + str(int_to_bytes(encryption_key)))
        else:
            print('\nAlice received message:')
            print('--- Ciphertext:\t', msg)
            print('--- Plaintext:\t', decrypt(msg, encryption_key))

        if msg == 'close':
            conn.close()
            break
    listener.close()

if __name__ == '__main__':
    '''
    listen on port
    exchange keys
    once final key is determined, send message
    decrypt received message
    '''
    listen(4000)
