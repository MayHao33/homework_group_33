from hashlib import sha256
from ecdsa import SigningKey, SECP256k1

def generate_sm2_keypair():
    #产生一个随机私钥
    private_key = SigningKey.generate(curve=SECP256k1)

    #计算对应公钥
    public_key = private_key.get_verifying_key()

    return private_key, public_key

def sm2_sign(private_key, message):
    #计算消息哈希值
    digest = sha256(message.encode()).digest()

    #使用RFC6979确定签名生成
    signature = private_key.sign_deterministic(digest, hashfunc=sha256)

    return signature

def sm2_verify(public_key, message, signature):
    #计算消息哈希值
    digest = sha256(message.encode()).digest()

    #验证签名
    try:
        result = public_key.verify(signature, digest, hashfunc=sha256)
        return result
    except:
        return False

private_key, public_key = generate_sm2_keypair()

message = "Hello, May!"
signature = sm2_sign(private_key, message)


valid = sm2_verify(public_key, message, signature)
print('Message:',message)
print('Signature:',signature)
print()
print(f"The signature is valid: {valid}")

#篡改签名，验证失败
signature = signature[:10] + b"\x01" + signature[11:]
valid = sm2_verify(public_key, message, signature)
print()
print('Tamper signature,then:')
print(f"The signature is valid: {valid}")
