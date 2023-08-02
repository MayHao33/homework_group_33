import hashlib
import struct

def sha256_padding(msg):
    ml = len(msg) * 8
    padding = b'\x80' + b'\x00' * ((56 - (len(msg) + 1) % 64) % 64)
    padding += struct.pack('>Q', ml)
    return padding

def sha256_hash(message):
    return hashlib.sha256(message).digest()

def length_extension_attack(original_msg, original_msg_hash, additional_msg):
    msg_length = len(original_msg)
    forged_msg_hash = original_msg_hash

    num_blocks = (msg_length + 8) // 64

    forged_msg = original_msg + sha256_padding(original_msg)[num_blocks*64:] + additional_msg
    forged_msg_hash = sha256_hash(forged_msg)

    return forged_msg, forged_msg_hash

original_msg = b'This is the original message'
additional_msg = b'This is the additional message'

original_msg_hash = sha256_hash(original_msg)
forged_msg, forged_msg_hash = length_extension_attack(original_msg, original_msg_hash, additional_msg)

print("Original Message:", original_msg)
print("Original Message hash:", original_msg_hash.hex())
print("Forged Message:", forged_msg)
print("Forged Message hash:", forged_msg_hash.hex())
