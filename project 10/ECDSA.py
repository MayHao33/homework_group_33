import ecdsa

# Generate private key
private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

# Get public key from private key
public_key = private_key.get_verifying_key()

# Generate a message to sign
message = "Hello,May！"

# Sign the message
signature = private_key.sign(message.encode())

# Verify the signature
is_valid = public_key.verify(signature, message.encode())

print("Message:", message)
print("Signature:", signature.hex())
print("Is Valid:", is_valid)
