"""
RSA Digital Signature Module (JOUR3_PARTIE2)

Purpose: Implement RSA digital signatures for message authentication and non-repudiation.

Architecture:
  - Each message is signed with sender's private key
  - Signature verifiable by anyone with sender's public key
  - Guarantees: authenticity, integrity, non-repudiation
  - Algorithm: RSA-PSS with PKCS1v15 and SHA256
  - Signature size: 256 bytes (matches 2048-bit key)

Example:
  # Sign a message
  signature_b64 = RSASignature.sign(private_key, "secret message")
  
  # Verify signature
  verified = RSASignature.verify(public_key, "secret message", signature_b64)
  assert verified

Security Properties:
  - Authenticity: Only signer can create valid signature
  - Integrity: Any bit change in message invalidates signature
  - Non-repudiation: Signer cannot deny creating the message
  - SHA256: Collision resistant hash
  - PSS padding: Probabilistic for semantic security
"""

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


class RSASignature:
    """RSA digital signature utilities for message authentication."""
    
    @staticmethod
    def sign(private_key, message):
        """
        Sign a message using RSA private key (PSS with SHA256).
        
        Args:
            private_key: RSA private key object
            message (str or bytes): Message to sign
        
        Returns:
            str: Base64-encoded signature
        
        Security:
            - Uses RSA-PSS padding (probabilistic)
            - SHA256 hash algorithm
            - Different signature each time (semantic security)
        
        Example:
            signature_b64 = RSASignature.sign(alice_private_key, "Hello Bob")
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        signature_bytes = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature_bytes).decode('ascii')
    
    @staticmethod
    def verify(public_key, message, signature_b64):
        """
        Verify a message signature using RSA public key.
        
        Args:
            public_key: RSA public key object
            message (str or bytes): Message to verify
            signature_b64 (str): Base64-encoded signature
        
        Returns:
            bool: True if signature is valid, False otherwise
        
        Security:
            - Returns False for invalid signature (exception caught)
            - Cannot forge signature without private key
            - Verifies both message integrity and signer identity
        
        Example:
            verified = RSASignature.verify(bob_public_key, "Hello Bob", signature_b64)
            if verified:
                print("Message from Alice is authentic!")
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        try:
            signature_bytes = base64.b64decode(signature_b64)
            public_key.verify(
                signature_bytes,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_signature_size():
        """
        Get signature size in bytes.
        
        For RSA-2048: 256 bytes (2048 bits / 8)
        
        Returns:
            int: Signature size in bytes
        """
        return 256  # RSA-2048 produces 256-byte signatures
