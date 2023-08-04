import hashlib

# 定义椭圆曲线参数
a = -3
b = 2455155546008943817740293915197451784769108058161191238065
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
G = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
     32670510020758816978083085130507043184471273380659243275938904335757337482424)


def point_addition(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if p1 == (0, 0):
        return p2
    if p2 == (0, 0):
        return p1
    if x1 == x2 and (y1 != y2 or y1 == 0):
        return (0, 0)
    if p1 == p2:
        m = (3 * x1 * x1 + a) * pow(2 * y1, p - 2, p)
    else:
        m = (y1 - y2) * pow(x1 - x2, p - 2, p)
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_multiplication(k, p):
    binary = bin(k)[2:][::-1]
    Q = (0, 0)
    for i, bit in enumerate(binary):
        if bit == '1':
            Q = point_addition(Q, p)
        p = point_addition(p, p)
    return Q


def ECMH(message):
    hash_value = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    point = scalar_multiplication(hash_value, G)
    return point


if __name__ == '__main__':
    message = 'Hello,May!'
    h = ECMH(message)
    print("ECMH('{}') = {}".format(message, h))
