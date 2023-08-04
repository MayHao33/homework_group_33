import base64
import binascii
import time
from gmssl import sm2, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

class PGP:
    def __init__(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key
        self.iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.crypt_sm4 = CryptSM4()
        self.sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)

    def encrypt(self, message, key):
        enc_data = self.sm2_crypt.encrypt(key)
        self.crypt_sm4.set_key(key, SM4_ENCRYPT)
        encrypt_value = self.crypt_sm4.crypt_cbc(self.iv, message)
        return encrypt_value, enc_data

    def decrypt(self, encrypt_value, enc_data):
        k = self.sm2_crypt.decrypt(enc_data)
        self.crypt_sm4.set_key(k, SM4_DECRYPT)
        decrypt_value = self.crypt_sm4.crypt_ecb(encrypt_value)
        return decrypt_value, k

if __name__ == '__main__':
    private_key = '56acc9b4e5065c7d60aa219c324d79246716bde4fcaf89254cb3f912c8c3282b5e'
    public_key = 'cb93852871e5acdd70fbaed4d69fc2cb86a1b01fa4494ad32bcc18f9110af98ae8ec4fd6865dda2f4096160341d9c9030fdeadbc6c01cd5f3784c7123ff92991'
    key = b'875555bd913d1031'
    message = b'HiMay'

    t1=time.time()
    pgp = PGP(private_key, public_key)
    encrypt_value, enc_data = pgp.encrypt(message, key)
    print("encrypt_value:", encrypt_value)
    print("enc_data:", enc_data)
    decrypt_value, k = pgp.decrypt(encrypt_value, enc_data)
    print("decrypt_value:", decrypt_value)
    print("k:", k)
    t2=time.time()
    print("用时:{}s".format(t2-t1))
