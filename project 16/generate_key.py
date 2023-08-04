from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_private_key():
    private_key = ec.generate_private_key(
        ec.SECP256R1()  # 或者使用其他的椭圆曲线参数
    )
    return private_key

def save_private_key(private_key):
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key.pem', 'wb') as key_file:
        key_file.write(private_key_pem)

def main():
    private_key = generate_private_key()
    save_private_key(private_key)

if __name__ == '__main__':
    main()
