import struct
import hashlib

def sm3_padding(msg):
    #消息填充，满足SM3算法要求
    ml = len(msg) * 8
    padding = b'\x80' + b'\x00' * ((56 - (len(msg) + 1) % 64) % 64)
    padding += struct.pack('>Q', ml)
    return padding

def sm3_hash(message):
    #利用hashlib库计算给定消息SM3哈希值
    return hashlib.new('sm3', message).digest()

def length_extension_attack(original_msg, original_msg_hash, additional_msg):
    #计算原始消息长度与分组块数
    msg_length = len(original_msg)
    forged_msg_hash = original_msg_hash

    #计算分组块数
    num_blocks = (msg_length + 8) // 64

    #执行长度扩展攻击
    forged_msg = additional_msg + sm3_padding(additional_msg + original_msg)[num_blocks*64:]
    forged_msg_hash += sm3_hash(forged_msg)

    return forged_msg, forged_msg_hash

original_msg = b'This is the original message'
additional_msg = b'This is the additional message'

original_msg_hash = sm3_hash(original_msg)
forged_msg, forged_msg_hash = length_extension_attack(original_msg, original_msg_hash, additional_msg)

print("Original Message:", original_msg)
print("Original Message hash:", original_msg_hash.hex())
print("Forged Message:", forged_msg)
print("Forged Message hash:", forged_msg_hash.hex())
