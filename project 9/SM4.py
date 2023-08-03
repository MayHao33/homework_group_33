import time
import struct


def left_shift(x, n):
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))


def sm4_key_schedule(key):
    rk = [0] * 32
    mk = [0] * 4
    k = [0] * 36

    mk[0] = struct.unpack(">I", key[0:4])[0]
    mk[1] = struct.unpack(">I", key[4:8])[0]
    mk[2] = struct.unpack(">I", key[8:12])[0]
    mk[3] = struct.unpack(">I", key[12:16])[0]

    k[0:4] = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]
    for i in range(4, 36):
        k[i] = k[i-4] ^ (left_shift(k[i-1], 13) ^ left_shift(k[i-1], 23)) ^ (left_shift(k[i-3], 3) ^ left_shift(k[i-3], 8)) ^ (left_shift(k[i-2], 1))

    for i in range(32):
        rk[i] = k[i+4] ^ (left_shift(k[i+1], 2) ^ left_shift(k[i+1], 10)) ^ (left_shift(k[i+2], 7) ^ left_shift(k[i+2], 18)) ^ (left_shift(k[i+3], 3) ^ left_shift(k[i+3], 7))

    return rk


def sm4_round(x, rk):
    tmp = x ^ (left_shift(x, 2) ^ left_shift(x, 10)) ^ (left_shift(x, 18) ^ left_shift(x, 24))
    tmp = tmp ^ left_shift((tmp & 0xFFFF), 9) ^ left_shift((tmp & 0xFFFF), 19)
    return tmp ^ rk


def sm4_encrypt(input_data, key):
    rk = sm4_key_schedule(key)

    output_data = bytearray()
    for i in range(0, len(input_data), 4):
        x = struct.unpack(">I", input_data[i:i+4])[0]
        for j in range(32):
            x = sm4_round(x, rk[j])
        output_data += struct.pack(">I", x)

    return output_data


def test_sm4_encrypt():
    input_data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x21\x00\x15\x00\x27'
    key = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x21\x00\x15\x00\x27'

    start_time = time.perf_counter()
    output_data = sm4_encrypt(input_data, key)
    end_time = time.perf_counter()

    print("明文:", input_data.hex())
    print("密文:", output_data.hex())
    print("一次加密时间:", end_time - start_time, "s")


if __name__ == "__main__":
    test_sm4_encrypt()
