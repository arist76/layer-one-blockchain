
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from hashlib import sha3_256

def generate_keys():
    """
    Generate a private key, public key, and Ethereum-compatible address.
    Returns:
        - private_key: The private key in hexadecimal format.
        - public_key: The uncompressed public key in hexadecimal format.
        - eth_address: The Ethereum address in hexadecimal format.
    """

    # Generate private key
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

    # Get public key
    public_key = private_key.public_key()
    public_numbers = public_key.public_numbers()
    x = public_numbers.x.to_bytes(32, byteorder='big')
    y = public_numbers.y.to_bytes(32, byteorder='big')
    uncompressed_public_key = b'\x04' + x + y

    # Compute Ethereum address
    keccak_hash = sha3_256()
    keccak_hash.update(uncompressed_public_key[1:])  # Exclude the first byte (0x04)

    # Convert keys and address to hexadecimal
    private_key_hex = private_key.private_numbers().private_value.to_bytes(32, byteorder='big').hex()
    public_key_hex = uncompressed_public_key.hex()

    return private_key_hex, public_key_hex

def sign_message(private_key_hex, message):
    """
    Sign a message using the private key.
    Args:
        - private_key_hex: Private key in hexadecimal format.
        - message: The message (bytes) to sign.
    Returns:
        - signature: The signature in bytes.
    """
    private_key_int = int(private_key_hex, 16)
    private_key = ec.derive_private_key(private_key_int, ec.SECP256K1(), default_backend())
    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
    return signature

def verify_message(public_key_hex, message, signature):
    """
    Verify a message signature using the public key.
    Args:
        - public_key_hex: Public key in hexadecimal format.
        - message: The message (bytes) to verify.
        - signature: The signature in bytes.
    Returns:
        - is_valid: Boolean indicating if the signature is valid.
    """
    x = int(public_key_hex[2:66], 16)  # Extract X coordinate
    y = int(public_key_hex[66:], 16)  # Extract Y coordinate
    public_key = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256K1()).public_key(default_backend())
    try:
        public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False

def hash_message(message):
    """
    Hash a message using Keccak-256.
    Args:
        - message: The message (bytes) to hash.
    Returns:
        - hash_hex: The hash in hexadecimal format.
    """
    keccak_hash = sha3_256()
    keccak_hash.update(message)
    return keccak_hash.hexdigest()

# Example Usage
if __name__ == "__main__":
    # Generate keys
    private_key, public_key = generate_keys()
    print("Private Key:", private_key)
    print("Public Key:", public_key)

    # Sign a message
    message = b"Hello, Ethereum!"
    signature = sign_message(private_key, message)
    print("Signature:", signature.hex())

    # Verify the message
    is_valid = verify_message(public_key, message, signature)
    print("Is the signature valid?", is_valid)

    # Hash the message
    message_hash = hash_message(message)
    print("Message Hash:", message_hash)
