"""
RSA Asymmetric Cryptography Module (JOUR3_PARTIE1)

Purpose: Implement RSA-based key exchange for end-to-end encryption.

Architecture:
  - Each user generates RSA 2048-bit keypair (public + private)
  - Public key is shared with server and other clients
  - Private key is stored locally and never transmitted
  - Key exchange: encrypt session_key with recipient's public key
  - Session_key decrypted only by recipient with their private key

Algorithm: RSA-2048 with OAEP padding (SHA256)
  - Key size: 2048 bits (256 bytes encrypted)
  - Padding: OAEP with MGF1-SHA256
  - Encoding: PEM for storage and transmission
  - Session keys: 256 bits (32 bytes)

Example:
  # Generate keypair
  private_key, public_key = RSACrypto.generate_keypair()
  
  # Serialize to PEM
  private_pem = RSACrypto.private_to_pem(private_key)
  public_pem = RSACrypto.public_to_pem(public_key)
  
  # Load from PEM
  private_key = RSACrypto.pem_to_private_key(private_pem)
  public_key = RSACrypto.pem_to_public_key(public_pem)
  
  # Encrypt session key
  session_key = os.urandom(32)
  encrypted_b64 = RSACrypto.encrypt_session_key(public_key, session_key)
  
  # Decrypt session key
  decrypted = RSACrypto.decrypt_session_key(private_key, encrypted_b64)
  assert decrypted == session_key
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base64
import os


class RSACrypto:
    """RSA cryptography utilities for key exchange and encapsulation."""
    
    KEY_SIZE = 2048  # bits (256 bytes)
    PUBLIC_EXPONENT = 65537
    
    @staticmethod
    def generate_keypair(key_size=KEY_SIZE):
        """
        Generate a new RSA keypair.
        
        Args:
            key_size (int): Key size in bits (default 2048)
        
        Returns:
            tuple: (private_key, public_key) objects
        
        Example:
            private_key, public_key = RSACrypto.generate_keypair()
        """
        private_key = rsa.generate_private_key(
            public_exponent=RSACrypto.PUBLIC_EXPONENT,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    @staticmethod
    def private_to_pem(private_key):
        """
        Serialize private key to PEM format.
        
        Args:
            private_key: RSA private key object
        
        Returns:
            bytes: PEM-encoded private key
        
        Format:
            -----BEGIN PRIVATE KEY-----
            MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
            ...
            -----END PRIVATE KEY-----
        """
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    
    @staticmethod
    def public_to_pem(public_key):
        """
        Serialize public key to PEM format.
        
        Args:
            public_key: RSA public key object
        
        Returns:
            bytes: PEM-encoded public key
        
        Format:
            -----BEGIN PUBLIC KEY-----
            MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBIjANBgkqhkiG9w0...
            ...
            -----END PUBLIC KEY-----
        """
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    @staticmethod
    def pem_to_private_key(pem_bytes):
        """
        Load private key from PEM format.
        
        Args:
            pem_bytes (bytes): PEM-encoded private key
        
        Returns:
            Private key object
        
        Example:
            pem_data = b'-----BEGIN PRIVATE KEY-----\\n...'
            private_key = RSACrypto.pem_to_private_key(pem_data)
        """
        return serialization.load_pem_private_key(
            pem_bytes,
            password=None,
            backend=default_backend()
        )
    
    @staticmethod
    def pem_to_public_key(pem_bytes):
        """
        Load public key from PEM format.
        
        Args:
            pem_bytes (bytes): PEM-encoded public key
        
        Returns:
            Public key object
        
        Example:
            pem_data = b'-----BEGIN PUBLIC KEY-----\\n...'
            public_key = RSACrypto.pem_to_public_key(pem_data)
        """
        return serialization.load_pem_public_key(
            pem_bytes,
            backend=default_backend()
        )
    
    @staticmethod
    def encrypt_session_key(public_key, session_key):
        """
        Encrypt session key using public key (key encapsulation).
        
        Args:
            public_key: RSA public key object
            session_key (bytes): Session key to encrypt (32 bytes for AES-256)
        
        Returns:
            str: Base64-encoded encrypted session key
        
        Security:
            - Uses RSA-OAEP with SHA256
            - MGF1 with SHA256
            - Provides semantic security (same input → different output)
            - Resistant to chosen plaintext attacks
        
        Example:
            session_key = os.urandom(32)
            encrypted_b64 = RSACrypto.encrypt_session_key(bob_public_key, session_key)
            # encrypted_b64 can be sent over insecure channel
        """
        ciphertext = public_key.encrypt(
            session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode('ascii')
    
    @staticmethod
    def decrypt_session_key(private_key, encrypted_session_key_b64):
        """
        Decrypt session key using private key (key decapsulation).
        
        Args:
            private_key: RSA private key object
            encrypted_session_key_b64 (str): Base64-encoded encrypted session key
        
        Returns:
            bytes: Decrypted session key (32 bytes)
        
        Raises:
            ValueError: If decryption fails (wrong key or corrupted data)
        
        Example:
            encrypted_b64 = "aBcD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0..."
            session_key = RSACrypto.decrypt_session_key(bob_private_key, encrypted_b64)
            # session_key == alice's session_key (shared secret)
        """
        encrypted_session_key = base64.b64decode(encrypted_session_key_b64)
        
        session_key = private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return session_key
    
    @staticmethod
    def get_key_size(public_key):
        """
        Get the key size in bits.
        
        Args:
            public_key: RSA public key object
        
        Returns:
            int: Key size in bits (e.g., 2048)
        """
        return public_key.key_size
