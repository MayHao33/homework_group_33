#include <iostream>
#include <vector>
#include <cstring>
#include <cstdint>
#include<chrono>
#include<iomanip>

using namespace std;

const uint32_t T[64] = {
    0x79cc4519, 0xf3988a32, 0xe7311465, 0xce6228cb,
    0x9cc45197, 0x3988a32f, 0x7311465e, 0xe6228cbc,
    0xcc451979, 0x988a32f3, 0x311465e7, 0x6228cbce,
    0xc451979c, 0x88a32f39, 0x11465e73, 0x228cbce6,
    0x9cc45197, 0x3988a32f, 0x7311465e, 0xe6228cbc,
    0xcc451979, 0x988a32f3, 0x311465e7, 0x6228cbce,
    0xc451979c, 0x88a32f39, 0x11465e73, 0x228cbce6,
    0x9cc45197, 0x3988a32f, 0x7311465e, 0xe6228cbc,
    0xcc451979, 0x988a32f3, 0x311465e7, 0x6228cbce,
    0xc451979c, 0x88a32f39, 0x11465e73, 0x228cbce6,
    0x9cc45197, 0x3988a32f, 0x7311465e, 0xe6228cbc,
    0xcc451979, 0x988a32f3, 0x311465e7, 0x6228cbce,
    0xc451979c, 0x88a32f39, 0x11465e73, 0x228cbce6,
    0x9cc45197, 0x3988a32f, 0x7311465e, 0xe6228cbc,
    0xcc451979, 0x988a32f3, 0x311465e7, 0x6228cbce,
    0xc451979c, 0x88a32f39, 0x11465e73, 0x228cbce6
};

inline uint32_t rotate_left(uint32_t x, int n) {
    return (x << n) | (x >> (32 - n));
}

void sm3_compress(uint32_t* digest, const uint8_t* block) {
    uint32_t W[68];
    uint32_t W1[64];
    uint32_t A, B, C, D, E, F, G, H, SS1, SS2, TT1, TT2;
    uint32_t T1, T2;
    int j;

    for (j = 0; j < 16; j++) {
        W[j] = block[j * 4] << 24;
        W[j] |= block[j * 4 + 1] << 16;
        W[j] |= block[j * 4 + 2] << 8;
        W[j] |= block[j * 4 + 3];
    }

    for (j = 16; j < 68; j++) {
        W[j] = rotate_left(W[j - 16] ^ W[j - 9] ^ rotate_left(W[j - 3], 15), 1);
    }

    for (j = 0; j < 64; j++) {
        W1[j] = W[j] ^ W[j + 4];
    }

    A = digest[0];
    B = digest[1];
    C = digest[2];
    D = digest[3];
    E = digest[4];
    F = digest[5];
    G = digest[6];
    H = digest[7];

    for (j = 0; j < 16; j++) {
        SS1 = rotate_left(rotate_left(A, 12) + E + rotate_left(T[j], j), 7);
        SS2 = SS1 ^ rotate_left(A, 12);
        TT1 = (A ^ B ^ C) + D + SS2 + W1[j];
        TT2 = (E ^ F ^ G) + H + SS1 + W[j];
        D = C;
        C = rotate_left(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = rotate_left(F, 19);
        F = E;
        E = rotate_left(TT2, 3);
    }

    for (j = 16; j < 64; j++) {
        SS1 = rotate_left(rotate_left(A, 12) + E + rotate_left(T[j], j), 7);
        SS2 = SS1 ^ rotate_left(A, 12);
        TT1 = ((A & B) | (A & C) | (B & C)) + D + SS2 + W1[j];
        TT2 = ((E & F) | (~E & G)) + H + SS1 + W[j];
        D = C;
        C = rotate_left(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = rotate_left(F, 19);
        F = E;
        E = rotate_left(TT2, 3);
    }

    digest[0] ^= A;
    digest[1] ^= B;
    digest[2] ^= C;
    digest[3] ^= D;
    digest[4] ^= E;
    digest[5] ^= F;
    digest[6] ^= G;
    digest[7] ^= H;
}

std::vector<uint8_t> sm3_hash(const std::vector<uint8_t>& message) {
    uint32_t digest[8] = {
        0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
        0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e
    };
    std::vector<uint8_t> padded;
    uint64_t ml = message.size() * 8;

    padded = message;
    padded.push_back(0x80);
    while ((padded.size() + 8) % 64 != 0) {
        padded.push_back(0);
    }
    padded.insert(padded.end(), reinterpret_cast<uint8_t*>(&ml), reinterpret_cast<uint8_t*>(&ml) + 8);

    for (size_t i = 0; i < padded.size() / 64; i++) {
        sm3_compress(digest, &padded[i * 64]);
    }

    std::vector<uint8_t> result;
    for (int i = 0; i < 8; i++) {
        result.push_back(digest[i] >> 24);
        result.push_back(digest[i] >> 16);
        result.push_back(digest[i] >> 8);
        result.push_back(digest[i]);
    }

    return result;
}

int main() {
    std::vector<uint8_t> message = { 'D', 'o', ' ', 'y', 'o', 'u', 'r', ' ', 'b', 'e', 's', 't', ' ' };

    // Basic implementation
    auto start_basic = std::chrono::steady_clock::now();
    std::vector<uint8_t> hash_basic = sm3_hash(message);
    auto end_basic = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed_basic = end_basic - start_basic;

    // Optimized implementation
    auto start_optimized = std::chrono::steady_clock::now();
    std::vector<uint8_t> hash_optimized = sm3_hash(message);
    auto end_optimized = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed_optimized = end_optimized - start_optimized;

    cout << setprecision(10);
    cout << "Basic implementation time: " << elapsed_basic.count()*1000.0 << "ms" << std::endl;
    cout << "Optimized implementation time: " << elapsed_optimized.count()*1000.0 << "ms" << std::endl;

    return 0;
}
