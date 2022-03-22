from multiprocessing.connection import Listener
from random import randrange

from encryptionlib import decrypt

# public variables
public_modulus_p = 2312
public_base_g = 5

alice_secret = randrange(1000, 2000)
alice_public = (public_base_g ** alice_secret) % public_modulus_p
secret_key = None

def listen(port):
    listener = Listener(('localhost', port))
    print('Alice listenting at port', port)
    print('Alice\'s secret:', alice_secret)
    conn = listener.accept()
    while True:
        msg = conn.recv()
        if str(msg).startswith('public:'):
            bob_public_key = int(msg.split('public:')[1])
            print('Alice received Bob\'s public key:', bob_public_key)
            conn.send('public:' + str(alice_public))

            secret_key = (bob_public_key ** alice_secret) % public_modulus_p
            print('Alice generated secret key:', secret_key)
        else:
            print('\n-- Alice received message: --')
            print('    Ciphertext:', msg)
            print('    Plaintext:', decrypt(msg, secret_key))

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
