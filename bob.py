from multiprocessing.connection import Client

from encryptionlib import encrypt

public_modulus_p = 23
public_base_g = 5

bob_secret = 3
bob_public = (public_base_g ** bob_secret) % public_modulus_p

def begin(port):
    conn = Client(('localhost', port))
    print('Bob connected to port', port)
    conn.send('public:' + str(bob_public))
    response = conn.recv()
    alice_public_key = int(response.split('public:')[1])
    print('Bob received Alice\'s public key:', alice_public_key)

    secret_key = (alice_public_key ** bob_secret) % public_modulus_p
    print('Bob generated secret key:', secret_key)

    while True:
        input_text = input('> ')
        conn.send(encrypt(input_text, secret_key))
        if input_text == 'close':
            break

    conn.close()

if __name__ == '__main__':
    begin(4000)

