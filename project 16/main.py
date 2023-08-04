from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import socket

# Load private key from a PEM file
def load_private_key():
    with open('private_key.pem', 'rb') as key_file:
        private_key_data = key_file.read()
    return load_pem_private_key(private_key_data, password=None)

# Establish network connection
def establish_connection():
    host = '127.0.0.1'
    port = 1234

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    print("Waiting for sender to connect...")
    conn, addr = s.accept()
    print(f"Connected to: {addr[0]}:{addr[1]}")

    return conn, s

# Receive ciphertext from the sender
def receive_ciphertext(conn):
    ciphertext = conn.recv(4096)
    return ciphertext

# Perform SM2 decryption
def decrypt_ciphertext(ciphertext, private_key):
    plaintext = private_key.decrypt(ciphertext,ec.ECIES(utils.Prehashed(hashes.SHA256())))
    return plaintext.decode()

# Close the network connection
def close_connection(conn, s):
    conn.close()
    s.close()

# Main function
def main():
    private_key = load_private_key()
    conn, s = establish_connection()
    ciphertext = receive_ciphertext(conn)
    plaintext = decrypt_ciphertext(ciphertext, private_key)
    print("Decrypted plaintext:", plaintext)
    close_connection(conn, s)

if __name__ == '__main__':
    main()
