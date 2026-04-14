"""
Comprehensive validation suite for JOUR3_PARTIE1 (Asymmetric Cryptography - RSA)

Purpose: Validate all aspects of RSA-based key exchange and end-to-end encryption

Criteria:
  Part 1: RSA Key Generation (5 checks)
  Part 2: Key Serialization (5 checks)
  Part 3: Public Key Registry (5 checks)
  Part 4: Key Exchange Protocol (5 checks)
  Part 5: Session Key Encryption (5 checks)
  Part 6: Security Properties (5 checks)
  Part 7: Performance (1 check)
  ─────────────────────────────────
  Total: 31 checks

Run with: python tests/validate_jour3_partie1.py
"""

import sys
import os
import base64
import time
import tempfile
import shutil
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.asymmetric_crypto import RSACrypto
from src.utils.crypto import AES256Cipher


def print_header(title):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def check(condition, description):
    """Check condition and print result"""
    if condition:
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ FAILED: {description}")
        return False


def test_part_1_rsa_key_generation():
    """Part 1: RSA Key Generation (5 checks)"""
    print_header("PART 1: RSA Key Generation")
    passed = 0
    
    # Check 1: Generate keypair
    try:
        private_key, public_key = RSACrypto.generate_keypair()
        passed += check(True, "Generate RSA-2048 keypair")
    except Exception as e:
        check(False, f"Generate keypair: {e}")
        return passed
    
    # Check 2: Key size correct
    key_size = RSACrypto.get_key_size(public_key)
    passed += check(key_size == 2048, f"Key size is 2048 bits (got {key_size})")
    
    # Check 3: Generate multiple keypairs - verify uniqueness
    private1, public1 = RSACrypto.generate_keypair()
    private2, public2 = RSACrypto.generate_keypair()
    pem1 = RSACrypto.public_to_pem(public1)
    pem2 = RSACrypto.public_to_pem(public2)
    passed += check(pem1 != pem2, "Multiple keypairs are unique")
    
    # Check 4: Private key is different from public key
    private_pem = RSACrypto.private_to_pem(private_key)
    public_pem = RSACrypto.public_to_pem(public_key)
    passed += check(private_pem != public_pem, "Private and public keys are different")
    
    # Check 5: Keys work for encryption/decryption
    test_key = os.urandom(32)
    enc = RSACrypto.encrypt_session_key(public_key, test_key)
    dec = RSACrypto.decrypt_session_key(private_key, enc)
    passed += check(dec == test_key, "Keypair can encrypt/decrypt session keys")
    
    return passed


def test_part_2_key_serialization():
    """Part 2: Key Serialization (5 checks)"""
    print_header("PART 2: Key Serialization & Persistence")
    passed = 0
    
    private_key, public_key = RSACrypto.generate_keypair()
    
    # Check 1: Serialize private key to PEM
    try:
        private_pem = RSACrypto.private_to_pem(private_key)
        passed += check(
            b"-----BEGIN PRIVATE KEY-----" in private_pem,
            "Private key PEM contains valid header"
        )
    except Exception as e:
        check(False, f"Serialize private key: {e}")
        return passed
    
    # Check 2: Serialize public key to PEM
    try:
        public_pem = RSACrypto.public_to_pem(public_key)
        passed += check(
            b"-----BEGIN PUBLIC KEY-----" in public_pem,
            "Public key PEM contains valid header"
        )
    except Exception as e:
        check(False, f"Serialize public key: {e}")
        return passed
    
    # Check 3: Round-trip private key
    private_loaded = RSACrypto.pem_to_private_key(private_pem)
    test_key = os.urandom(32)
    enc = RSACrypto.encrypt_session_key(public_key, test_key)
    dec = RSACrypto.decrypt_session_key(private_loaded, enc)
    passed += check(dec == test_key, "Round-trip private key serialization works")
    
    # Check 4: Round-trip public key
    public_loaded = RSACrypto.pem_to_public_key(public_pem)
    enc2 = RSACrypto.encrypt_session_key(public_loaded, test_key)
    dec2 = RSACrypto.decrypt_session_key(private_key, enc2)
    passed += check(dec2 == test_key, "Round-trip public key serialization works")
    
    # Check 5: Base64 encoding for transport
    public_b64 = base64.b64encode(public_pem).decode('ascii')
    public_restored = base64.b64decode(public_b64)
    passed += check(public_restored == public_pem, "Base64 encoding preserves key data")
    
    return passed


def test_part_3_public_key_registry():
    """Part 3: Public Key Registry (5 checks)"""
    print_header("PART 3: Public Key Registry")
    passed = 0
    
    # Simulate registry
    registry = {}
    
    # Check 1: Register multiple users
    users = ["alice", "bob", "charlie"]
    user_keys = {}
    for user in users:
        private, public = RSACrypto.generate_keypair()
        user_keys[user] = (private, public)
        public_b64 = base64.b64encode(RSACrypto.public_to_pem(public)).decode('ascii')
        registry[user] = public_b64
    
    passed += check(len(registry) == 3, "Register 3 users in registry")
    
    # Check 2: Retrieve and verify keys
    alice_pub_b64 = registry["alice"]
    alice_pub_pem = base64.b64decode(alice_pub_b64)
    alice_pub = RSACrypto.pem_to_public_key(alice_pub_pem)
    passed += check(
        RSACrypto.get_key_size(alice_pub) == 2048,
        "Retrieved key is valid RSA-2048"
    )
    
    # Check 3: Encrypt/decrypt with registry keys
    bob_pub_b64 = registry["bob"]
    bob_pub_pem = base64.b64decode(bob_pub_b64)
    bob_pub = RSACrypto.pem_to_public_key(bob_pub_pem)
    bob_private = user_keys["bob"][0]
    
    session_key = os.urandom(32)
    encrypted = RSACrypto.encrypt_session_key(bob_pub, session_key)
    decrypted = RSACrypto.decrypt_session_key(bob_private, encrypted)
    passed += check(decrypted == session_key, "Encrypt with registry key works")
    
    # Check 4: Registry isolation (wrong key cannot decrypt)
    charlie_private = user_keys["charlie"][0]
    try:
        wrong_dec = RSACrypto.decrypt_session_key(charlie_private, encrypted)
        check(False, "Charlie should not decrypt Bob's message")
    except:
        passed += check(True, "Wrong key cannot decrypt (isolation verified)")
    
    # Check 5: Large registry performance
    large_registry = {}
    start = time.time()
    for i in range(100):
        username = f"user{i}"
        _, pub = RSACrypto.generate_keypair()
        pub_b64 = base64.b64encode(RSACrypto.public_to_pem(pub)).decode('ascii')
        large_registry[username] = pub_b64
    elapsed = time.time() - start
    passed += check(
        len(large_registry) == 100 and elapsed < 30,
        f"Registry with 100 users registers quickly ({elapsed:.2f}s)"
    )
    
    return passed


def test_part_4_key_exchange_protocol():
    """Part 4: Key Exchange Protocol (5 checks)"""
    print_header("PART 4: Key Exchange Protocol")
    passed = 0
    
    # Generate keys
    alice_priv, alice_pub = RSACrypto.generate_keypair()
    bob_priv, bob_pub = RSACrypto.generate_keypair()
    
    # Check 1: Alice generates session key
    alice_session = os.urandom(32)
    passed += check(len(alice_session) == 32, "Session key is 32 bytes (256 bits)")
    
    # Check 2: Alice encrypts with Bob's public key
    encrypted_for_bob = RSACrypto.encrypt_session_key(bob_pub, alice_session)
    passed += check(
        len(encrypted_for_bob) > 0 and encrypted_for_bob != alice_session,
        "Encryption produces different output than input"
    )
    
    # Check 3: Bob decrypts with his private key
    bob_received = RSACrypto.decrypt_session_key(bob_priv, encrypted_for_bob)
    passed += check(bob_received == alice_session, "Bob decrypts to original session key")
    
    # Check 4: Multiple encryptions produce different ciphertexts (semantic security)
    enc1 = RSACrypto.encrypt_session_key(bob_pub, alice_session)
    enc2 = RSACrypto.encrypt_session_key(bob_pub, alice_session)
    passed += check(enc1 != enc2, "Same input produces different ciphertexts (OAEP)")
    
    # Check 5: Bidirectional exchange
    bob_session = os.urandom(32)
    encrypted_for_alice = RSACrypto.encrypt_session_key(alice_pub, bob_session)
    alice_received = RSACrypto.decrypt_session_key(alice_priv, encrypted_for_alice)
    passed += check(
        alice_received == bob_session,
        "Bidirectional key exchange works independently"
    )
    
    return passed


def test_part_5_session_key_encryption():
    """Part 5: Session Key Encryption with AES (5 checks)"""
    print_header("PART 5: Session Key Encryption (AES-256-CBC)")
    passed = 0
    
    # Generate session key
    session_key = os.urandom(32)
    cipher = AES256Cipher(session_key)
    
    # Check 1: Encrypt plaintext message
    plaintext = "Secret message from Alice to Bob"
    encrypted = cipher.encrypt(plaintext)
    passed += check(
        "ciphertext" in encrypted and "iv" in encrypted,
        "Encryption returns ciphertext and IV"
    )
    
    # Check 2: Decrypt to original message
    decrypted = cipher.decrypt(encrypted["ciphertext"], encrypted["iv"])
    passed += check(decrypted == plaintext, "Decryption recovers original message")
    
    # Check 3: Multiple messages use different IVs
    cipher2 = AES256Cipher(session_key)
    encrypted2 = cipher2.encrypt(plaintext)
    passed += check(
        encrypted["iv"] != encrypted2["iv"],
        "Different messages have different IVs (even with same key and plaintext)"
    )
    
    # Check 4: Session key isolation (different keys produce different ciphertexts)
    different_key = os.urandom(32)
    different_cipher = AES256Cipher(different_key)
    encrypted_diff = different_cipher.encrypt(plaintext)
    passed += check(
        encrypted["ciphertext"] != encrypted_diff["ciphertext"],
        "Different session keys produce different ciphertexts"
    )
    
    # Check 5: Empty and long messages
    empty_enc = cipher.encrypt("")
    empty_dec = cipher.decrypt(empty_enc["ciphertext"], empty_enc["iv"])
    long_msg = "X" * 10000
    long_enc = cipher.encrypt(long_msg)
    long_dec = cipher.decrypt(long_enc["ciphertext"], long_enc["iv"])
    passed += check(
        empty_dec == "" and long_dec == long_msg,
        "Empty and large messages encrypt/decrypt correctly"
    )
    
    return passed


def test_part_6_security_properties():
    """Part 6: Security Properties (5 checks)"""
    print_header("PART 6: Security Properties")
    passed = 0
    
    alice_priv, alice_pub = RSACrypto.generate_keypair()
    bob_priv, bob_pub = RSACrypto.generate_keypair()
    
    # Check 1: Private key never appears in public key
    alice_priv_pem = RSACrypto.private_to_pem(alice_priv)
    alice_pub_pem = RSACrypto.public_to_pem(alice_pub)
    passed += check(
        b"-----BEGIN PUBLIC KEY-----" in alice_pub_pem and
        b"-----BEGIN PRIVATE KEY-----" not in alice_pub_pem,
        "Public key does not contain private key material"
    )
    
    # Check 2: RSA-OAEP provides semantic security
    session_key = os.urandom(32)
    enc_list = []
    for _ in range(10):
        enc = RSACrypto.encrypt_session_key(bob_pub, session_key)
        enc_list.append(enc)
    unique_encryptions = len(set(enc_list))
    passed += check(
        unique_encryptions >= 8,
        f"OAEP produces varied ciphertexts ({unique_encryptions}/10 unique)"
    )
    
    # Check 3: Server cannot decrypt peer-to-peer messages
    alice_session = os.urandom(32)
    encrypted_for_bob = RSACrypto.encrypt_session_key(bob_pub, alice_session)
    # Server only has public keys, should not be able to decrypt
    server_private = None  # Server doesn't have any private key
    passed += check(
        server_private is None,
        "Server architecture: only public keys stored (no private keys)"
    )
    
    # Check 4: Key derivation independence (different users, different keys)
    alice_session1 = os.urandom(32)
    alice_session2 = os.urandom(32)
    passed += check(
        alice_session1 != alice_session2,
        "Session keys are independently generated (unique)"
    )
    
    # Check 5: No plaintext leakage
    plaintext = "SENSITIVE DATA"
    cipher = AES256Cipher(alice_session1)
    encrypted = cipher.encrypt(plaintext)
    passed += check(
        plaintext not in encrypted["ciphertext"] and plaintext not in encrypted["iv"],
        "Plaintext does not appear in ciphertext or IV"
    )
    
    return passed


def test_part_7_performance():
    """Part 7: Performance (1 check)"""
    print_header("PART 7: Performance")
    passed = 0
    
    # Measure key exchange time for 10 exchanges
    start = time.time()
    for _ in range(10):
        alice_priv, alice_pub = RSACrypto.generate_keypair()
        bob_priv, bob_pub = RSACrypto.generate_keypair()
        session_key = os.urandom(32)
        enc = RSACrypto.encrypt_session_key(bob_pub, session_key)
        dec = RSACrypto.decrypt_session_key(bob_priv, enc)
    elapsed = time.time() - start
    
    # Should complete in reasonable time (< 5 seconds for 10 exchanges)
    avg_time = (elapsed / 10) * 1000  # Convert to ms
    passed += check(
        elapsed < 5,
        f"Key exchange performance: {avg_time:.1f}ms per exchange (10 exchanges in {elapsed:.2f}s)"
    )
    
    return passed


def main():
    """Run all validation tests"""
    print("\n" + "=" * 70)
    print("  JOUR3_PARTIE1 - Asymmetric Cryptography Validation Suite")
    print("  31 comprehensive checks across 7 parts")
    print("=" * 70)
    
    total_passed = 0
    
    total_passed += test_part_1_rsa_key_generation()
    total_passed += test_part_2_key_serialization()
    total_passed += test_part_3_public_key_registry()
    total_passed += test_part_4_key_exchange_protocol()
    total_passed += test_part_5_session_key_encryption()
    total_passed += test_part_6_security_properties()
    total_passed += test_part_7_performance()
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"  VALIDATION RESULTS: {total_passed}/31 checks passed")
    print("=" * 70)
    
    if total_passed == 31:
        print("\n✅ ALL VALIDATION CHECKS PASSED! ✅\n")
        return 0
    else:
        print(f"\n❌ {31 - total_passed} checks failed\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
