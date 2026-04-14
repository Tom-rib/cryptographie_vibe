"""
AES-256-CBC Symmetric Encryption Module.

Purpose: Encrypt and decrypt messages using AES (Advanced Encryption Standard)
with 256-bit keys in CBC (Cipher Block Chaining) mode.

Algorithm: AES-256-CBC
  - Key size: 256 bits (32 bytes)
  - IV (Initialization Vector): 128 bits (16 bytes), random per message
  - Mode: CBC (Cipher Block Chaining) - each block depends on previous
  - Padding: PKCS7 (automatic, adds padding bytes to reach 16-byte blocks)
  - Important: NEW IV for EVERY message (never reuse!)

Encoding: All binary data (ciphertext, IV) is base64-encoded for JSON transport

Example:
  key = os.urandom(32)  # 256-bit key
  cipher = AES256Cipher(key)
  
  # Encrypt a message
  result = cipher.encrypt("Hello Bob!")
  # result = {"ciphertext": "aBcD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0...", 
  #           "iv": "1iJ4kL5mN6oP7qR8sT9uV0wX1yZ2aB3c="}
  
  # Decrypt later with same key + IV
  plaintext = cipher.decrypt(result["ciphertext"], result["iv"])
  # plaintext = "Hello Bob!"
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64


class AES256Cipher:
    """
    Symmetric encryption/decryption using AES-256-CBC.
    
    Each instance is tied to a specific 256-bit encryption key.
    Every encrypt() call generates a new random IV and produces different output
    (even for same plaintext) - this is essential for security.
    """
    
    KEY_SIZE = 32  # 256 bits
    IV_SIZE = 16   # 128 bits
    
    def __init__(self, key):
        """
        Initialize cipher with a 256-bit key.
        
        Args:
            key (bytes): Must be exactly 32 bytes (256 bits)
        
        Raises:
            ValueError: If key is not 32 bytes
        
        Example:
            key, _ = KeyDerivation.derive("password123")
            cipher = AES256Cipher(key)
        """
        if len(key) != self.KEY_SIZE:
            raise ValueError(f"Key must be exactly {self.KEY_SIZE} bytes, got {len(key)}")
        
        self.key = key
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext to ciphertext + IV (both base64-encoded).
        
        Args:
            plaintext (str): Message to encrypt
        
        Returns:
            dict: {
                "ciphertext": str (base64-encoded ciphertext),
                "iv": str (base64-encoded IV)
            }
        
        Important:
            - A new random IV is generated for EVERY call
            - Even encrypting same plaintext twice produces different output
            - This randomization is cryptographically essential (prevents patterns)
        
        Example:
            result = cipher.encrypt("Secret message")
            print(result["ciphertext"])  # Different output each time!
            print(result["iv"])          # Different IV each time!
        """
        # Generate random IV (Initialization Vector)
        iv = os.urandom(self.IV_SIZE)
        
        # Apply PKCS7 padding (required for CBC mode)
        padder = padding.PKCS7(128).padder()
        plaintext_bytes = plaintext.encode('utf-8')
        padded_plaintext = padder.update(plaintext_bytes) + padder.finalize()
        
        # Create AES cipher in CBC mode
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        
        # Encrypt padded plaintext
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        
        # Return both ciphertext and IV as base64 (for JSON)
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('ascii'),
            'iv': base64.b64encode(iv).decode('ascii')
        }
    
    def decrypt(self, ciphertext_b64, iv_b64):
        """
        Decrypt ciphertext using the provided IV.
        
        Args:
            ciphertext_b64 (str): Base64-encoded ciphertext
            iv_b64 (str): Base64-encoded IV
        
        Returns:
            str: Decrypted plaintext
        
        Raises:
            ValueError: If decryption fails (wrong key, corrupted data, etc.)
        
        Important:
            - The IV used here must be the EXACT IV from encryption
            - If IV is wrong, decryption produces garbage (no error!)
            - Always use the IV stored with the ciphertext
        
        Example:
            plaintext = cipher.decrypt(result["ciphertext"], result["iv"])
            print(plaintext)  # "Secret message"
        """
        # Decode base64 to binary
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)
        
        # Validate IV length
        if len(iv) != self.IV_SIZE:
            raise ValueError(f"IV must be exactly {self.IV_SIZE} bytes, got {len(iv)}")
        
        # Create AES cipher in CBC mode with SAME IV as encryption
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        
        # Decrypt ciphertext
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove PKCS7 padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        # Return as UTF-8 string
        return plaintext_bytes.decode('utf-8')
