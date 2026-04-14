"""
Key Derivation Function (KDF) using PBKDF2 with SHA256.

Purpose: Derive a cryptographic key from a password deterministically.
This allows the same password to always produce the same encryption key.

Algorithm: PBKDF2 (Password-Based Key Derivation Function 2)
  - Hash function: SHA256
  - Iterations: 100,000 (slows down brute-force attacks)
  - Salt size: 128 bits (16 bytes) - unique per user
  - Output key size: 256 bits (32 bytes) - for AES-256

Example:
  password = "SecureP@ss123!"
  salt = os.urandom(16)  # Generate random salt
  key, salt = KeyDerivation.derive(password, salt)
  
  # Later, can re-derive the same key using the stored salt:
  key = KeyDerivation.derive_with_salt(password, salt_b64)
"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64


class KeyDerivation:
    """
    Utility class for deriving encryption keys from passwords using PBKDF2.
    
    Class Constants:
      - ITERATIONS: Number of PBKDF2 iterations (higher = more secure but slower)
      - KEY_SIZE: Output key size in bytes (256 bits = 32 bytes for AES-256)
      - SALT_SIZE: Random salt size in bytes (128 bits = 16 bytes, per spec)
    """
    
    ITERATIONS = 100000  # Per JOUR2_PARTIE2 spec
    KEY_SIZE = 32        # 256 bits for AES-256
    SALT_SIZE = 16       # 128 bits, unique per user
    
    @staticmethod
    def derive(password, salt=None):
        """
        Derive a key from a password, optionally generating a new salt.
        
        Args:
            password (str): The password to derive from
            salt (bytes): Optional existing salt. If None, generates new random salt.
        
        Returns:
            tuple: (key_bytes, salt_bytes)
                - key_bytes: 32-byte derived key (256 bits)
                - salt_bytes: 16-byte salt used (for storage)
        
        Example:
            key, salt = KeyDerivation.derive("password123")
            # key is 32 bytes, salt is 16 bytes (random)
            
            # To regenerate same key with same salt:
            key2, _ = KeyDerivation.derive("password123", salt)
            # key == key2 (deterministic when salt is same)
        """
        if salt is None:
            salt = os.urandom(KeyDerivation.SALT_SIZE)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KeyDerivation.KEY_SIZE,
            salt=salt,
            iterations=KeyDerivation.ITERATIONS,
            backend=default_backend()
        )
        
        key = kdf.derive(password.encode('utf-8'))
        return key, salt
    
    @staticmethod
    def derive_with_salt(password, salt_b64):
        """
        Derive a key from a password using an existing salt (base64-encoded).
        
        This is used when logging in: we already have the salt from signup,
        so we recreate the same key by deriving from password + known salt.
        
        Args:
            password (str): The password to derive from
            salt_b64 (str): Base64-encoded salt (from server storage)
        
        Returns:
            bytes: 32-byte derived key (256 bits)
        
        Example:
            # On signup: key, salt = derive("password")
            # Store: username:salt_b64
            
            # On login: key = derive_with_salt("password", stored_salt_b64)
            # key is identical to signup key (allows decryption of old messages)
        """
        salt = base64.b64decode(salt_b64)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KeyDerivation.KEY_SIZE,
            salt=salt,
            iterations=KeyDerivation.ITERATIONS,
            backend=default_backend()
        )
        
        return kdf.derive(password.encode('utf-8'))
