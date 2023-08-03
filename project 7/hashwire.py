import hashlib

def sha256(input):
    #对输入字符串执行SHA-256哈希
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

def generate_credential_chain(initial_value, num_credentials):
    #生成HashWires链
    credential_chain = []
    current_value = initial_value

    for _ in range(num_credentials):
        next_value = sha256(current_value)
        credential_chain.append(next_value)
        current_value = next_value

    return credential_chain

def verify_range_proof(credential_chain, proof_value, min_value, max_value):
    #进行范围证明
    counter = 0
    current_value = proof_value

    for credential in credential_chain:
        if current_value == credential:
            #如果证明值与凭证匹配，检查它是否在范围内
            return min_value <= counter <= max_value

        current_value = sha256(current_value)
        counter += 1

    return False #如果没有找到匹配项，则范围证明无效

if __name__ == "__main__":
    initial_value = "initial value"
    num_credentials = 10

    credential_chain = generate_credential_chain(initial_value, num_credentials)

    print("Credential Chain:")
    for credential in credential_chain:
        print(credential)

    #执行一次范围证明
    proof_value = credential_chain[5]
    min_value = 3
    max_value = 7

    is_range_valid = verify_range_proof(credential_chain, proof_value, min_value, max_value)

    if is_range_valid:
        print("Range proof is valid!")
    else:
        print("Range proof is invalid!")
