from ecdsa import SigningKey, VerifyingKey, SECP256k1


def generate_key():
    """
    Generate a new private key and its corresponding public key.

    Returns:
        tuple: A tuple containing the private key (hex) and public key (hex).
    """
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    private_key_hex = private_key.to_string().hex()
    public_key_hex = public_key.to_string().hex()
    return private_key_hex, public_key_hex


def sign_message(private_key_hex, message):
    """
    Sign a message using the given private key.

    Args:
        private_key_hex (str): The private key in hexadecimal format.
        message (str): The message to be signed.

    Returns:
        str: The signature in hexadecimal format.
    """
    private_key_bytes = bytes.fromhex(private_key_hex)
    private_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    signature = private_key.sign(message.encode())
    return signature.hex()


def verify_signature(public_key_hex, message, signature):
    """
    Verify a signature against a message and a public key.

    Args:
        public_key_hex (str): The public key in hexadecimal format.
        message (str): The original message.
        signature (str): The signature in hexadecimal format.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    public_key_bytes = bytes.fromhex(public_key_hex)
    public_key = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)
    try:
        return public_key.verify(bytes.fromhex(signature), message.encode())
    except:
        return False


if __name__ == "__main__":
    private_key_hex, public_key_hex = generate_key()
    print("Private Key (Hex):", private_key_hex)
    print("Public Key (Hex):", public_key_hex)

    message = "Hello, Ethereum!"
    signature = sign_message(private_key_hex, message)
    print("Signature:", signature)

    is_valid = verify_signature(public_key_hex, message, signature)
    print("Signature Valid:", is_valid)
