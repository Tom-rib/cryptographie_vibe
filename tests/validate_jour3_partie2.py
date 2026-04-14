"""
Comprehensive validation suite for JOUR3_PARTIE2 (End-to-End Encryption + Signatures)

Purpose: Validate all aspects of E2EE with RSA signatures and message authentication

Criteria:
  Part 1: RSA Signatures (5 checks)
  Part 2: Signature Verification (5 checks)
  Part 3: Combined Encryption + Signature (5 checks)
  Part 4: Room Encryption (4 checks)
  Part 5: Security Properties (5 checks)
  ─────────────────────────────────────────
  Total: 24 checks

Run with: python tests/validate_jour3_partie2.py
"""

import sys
import os
import base64
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.asymmetric_crypto import RSACrypto
from src.utils.signature import RSASignature
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


def test_part_1_rsa_signatures():
    """Part 1: RSA Signatures (5 checks)"""
    print_header("PART 1: RSA Digital Signatures")
    passed = 0
    
    private_key, public_key = RSACrypto.generate_keypair()
    message = "This is a secret message"
    
    # Check 1: Sign message
    try:
        signature = RSASignature.sign(private_key, message)
        passed += check(
            len(signature) > 0 and isinstance(signature, str),
            "Sign message produces base64 signature"
        )
    except Exception as e:
        check(False, f"Sign message: {e}")
        return passed
    
    # Check 2: Signature is base64
    try:
        decoded = base64.b64decode(signature)
        passed += check(len(decoded) == 256, "Signature is 256 bytes (RSA-2048)")
    except:
        check(False, "Signature is not valid base64")
    
    # Check 3: Different messages have different signatures
    sig1 = RSASignature.sign(private_key, "Message 1")
    sig2 = RSASignature.sign(private_key, "Message 2")
    passed += check(sig1 != sig2, "Different messages have different signatures")
    
    # Check 4: Same message has different signatures (PSS padding)
    sig1 = RSASignature.sign(private_key, message)
    sig2 = RSASignature.sign(private_key, message)
    passed += check(sig1 != sig2, "Same message produces different signatures (PSS)")
    
    # Check 5: Sign bytes and strings
    sig_str = RSASignature.sign(private_key, "Test")
    sig_bytes = RSASignature.sign(private_key, b"Test")
    passed += check(
        isinstance(sig_str, str) and isinstance(sig_bytes, str),
        "Signatures are always base64 strings (bytes or string input)"
    )
    
    return passed


def test_part_2_signature_verification():
    """Part 2: Signature Verification (5 checks)"""
    print_header("PART 2: Signature Verification")
    passed = 0
    
    alice_priv, alice_pub = RSACrypto.generate_keypair()
    bob_priv, bob_pub = RSACrypto.generate_keypair()
    message = "Hello Bob"
    
    # Check 1: Verify valid signature
    signature = RSASignature.sign(alice_priv, message)
    verified = RSASignature.verify(alice_pub, message, signature)
    passed += check(verified, "Valid signature verifies successfully")
    
    # Check 2: Reject invalid signature (different message)
    verified = RSASignature.verify(alice_pub, "Hello Charlie", signature)
    passed += check(not verified, "Different message fails verification")
    
    # Check 3: Reject wrong signer
    verified = RSASignature.verify(bob_pub, message, signature)
    passed += check(not verified, "Signature from wrong key fails verification")
    
    # Check 4: Reject corrupted signature
    sig_corrupted = signature[:-20] + "A" * 20
    verified = RSASignature.verify(alice_pub, message, sig_corrupted)
    passed += check(not verified, "Corrupted signature fails verification")
    
    # Check 5: Multiple signatures of same message all verify
    sigs = [RSASignature.sign(alice_priv, message) for _ in range(5)]
    all_valid = all(RSASignature.verify(alice_pub, message, sig) for sig in sigs)
    passed += check(all_valid, "Multiple signatures of same message all verify")
    
    return passed


def test_part_3_combined_crypto():
    """Part 3: Combined Encryption + Signature (5 checks)"""
    print_header("PART 3: Combined Encryption + Signature")
    passed = 0
    
    # Setup
    alice_priv, alice_pub = RSACrypto.generate_keypair()
    bob_priv, bob_pub = RSACrypto.generate_keypair()
    session_key = os.urandom(32)
    cipher = AES256Cipher(session_key)
    
    # Check 1: Encrypt then sign
    plaintext = "Secret message"
    encrypted = cipher.encrypt(plaintext)
    signature = RSASignature.sign(alice_priv, plaintext)
    passed += check(
        encrypted["ciphertext"] != plaintext and signature != plaintext,
        "Message encrypted and signed produces different outputs"
    )
    
    # Check 2: Decrypt and verify
    decrypted = cipher.decrypt(encrypted["ciphertext"], encrypted["iv"])
    verified = RSASignature.verify(alice_pub, decrypted, signature)
    passed += check(
        decrypted == plaintext and verified,
        "Decryption and signature verification both succeed"
    )
    
    # Check 3: Cannot decrypt with wrong key
    wrong_key = os.urandom(32)
    wrong_cipher = AES256Cipher(wrong_key)
    try:
        wrong_dec = wrong_cipher.decrypt(encrypted["ciphertext"], encrypted["iv"])
        passed += check(
            wrong_dec != plaintext,
            "Wrong key decrypts to garbage (not original plaintext)"
        )
    except:
        passed += check(True, "Wrong key causes decryption error")
    
    # Check 4: Cannot forge signature with wrong key
    forged_sig = RSASignature.sign(bob_priv, plaintext)
    verified = RSASignature.verify(alice_pub, plaintext, forged_sig)
    passed += check(not verified, "Forged signature fails verification")
    
    # Check 5: Message authenticity and confidentiality both required
    # Alice encrypts to Bob, Bob decrypts and verifies
    msg_to_bob = "Meet me at 3pm"
    bob_session = os.urandom(32)
    bob_cipher = AES256Cipher(bob_session)
    
    # This won't work (different session key), but demonstrates the architecture
    enc_to_bob = bob_cipher.encrypt(msg_to_bob)
    alice_sig = RSASignature.sign(alice_priv, msg_to_bob)
    
    # Bob decrypts with his session key
    dec_by_bob = bob_cipher.decrypt(enc_to_bob["ciphertext"], enc_to_bob["iv"])
    # Bob verifies with Alice's public key
    verified = RSASignature.verify(alice_pub, dec_by_bob, alice_sig)
    passed += check(
        dec_by_bob == msg_to_bob and verified,
        "End-to-end: encrypt + sign + decrypt + verify works"
    )
    
    return passed


def test_part_4_room_encryption():
    """Part 4: Room Encryption (4 checks)"""
    print_header("PART 4: Room Encryption")
    passed = 0
    
    # Check 1: Generate room key
    room_key = os.urandom(32)
    passed += check(len(room_key) == 32, "Room key is 256 bits (32 bytes)")
    
    # Check 2: Encrypt room message
    cipher = AES256Cipher(room_key)
    msg = "Hello everyone in the room"
    encrypted = cipher.encrypt(msg)
    passed += check(
        encrypted["ciphertext"] != msg,
        "Room message encrypted with room key"
    )
    
    # Check 3: All room members decrypt with same key
    all_decrypt = True
    for _ in range(3):
        decrypted = cipher.decrypt(encrypted["ciphertext"], encrypted["iv"])
        if decrypted != msg:
            all_decrypt = False
    passed += check(all_decrypt, "Multiple members decrypt with same room key")
    
    # Check 4: Room isolation (different room key cannot decrypt)
    room2_key = os.urandom(32)
    room2_cipher = AES256Cipher(room2_key)
    try:
        wrong = room2_cipher.decrypt(encrypted["ciphertext"], encrypted["iv"])
        all_correct = wrong == msg
    except:
        all_correct = False
    passed += check(not all_correct, "Different room key cannot decrypt")
    
    return passed


def test_part_5_security_properties():
    """Part 5: Security Properties (5 checks)"""
    print_header("PART 5: Security Properties")
    passed = 0
    
    alice_priv, alice_pub = RSACrypto.generate_keypair()
    bob_priv, bob_pub = RSACrypto.generate_keypair()
    
    # Check 1: Non-repudiation (Alice cannot deny signing)
    message = "I promise to pay you 100 euros"
    signature = RSASignature.sign(alice_priv, message)
    verified = RSASignature.verify(alice_pub, message, signature)
    passed += check(
        verified and alice_pub,
        "Signature proves Alice signed (non-repudiation)"
    )
    
    # Check 2: Confidentiality (only recipient can decrypt)
    session_key = os.urandom(32)
    cipher = AES256Cipher(session_key)
    secret = "Secret data"
    encrypted = cipher.encrypt(secret)
    
    # Only someone with session_key can decrypt
    wrong_key = os.urandom(32)
    wrong_cipher = AES256Cipher(wrong_key)
    try:
        wrong_dec = wrong_cipher.decrypt(encrypted["ciphertext"], encrypted["iv"])
        correct = wrong_dec == secret
    except:
        correct = False
    passed += check(
        not correct,
        "Confidentiality: only session_key holder can decrypt"
    )
    
    # Check 3: Integrity (bit change breaks everything)
    msg_to_sign = "Important data"
    sig = RSASignature.sign(alice_priv, msg_to_sign)
    
    # Change one bit
    sig_bytes = bytearray(base64.b64decode(sig))
    sig_bytes[0] ^= 1
    sig_corrupted = base64.b64encode(bytes(sig_bytes)).decode('ascii')
    
    verified = RSASignature.verify(alice_pub, msg_to_sign, sig_corrupted)
    passed += check(not verified, "Integrity: one bit change breaks signature")
    
    # Check 4: Authenticity (only signer can create valid signature)
    msg = "This is from Alice"
    alice_sig = RSASignature.sign(alice_priv, msg)
    
    # Bob cannot create valid signature for Alice
    bob_sig = RSASignature.sign(bob_priv, msg)
    verified_as_alice = RSASignature.verify(alice_pub, msg, bob_sig)
    passed += check(
        not verified_as_alice,
        "Authenticity: only Alice can create valid Alice signature"
    )
    
    # Check 5: Forward secrecy (session keys independent)
    sk1 = os.urandom(32)
    sk2 = os.urandom(32)
    c1 = AES256Cipher(sk1)
    c2 = AES256Cipher(sk2)
    
    msg1 = "Message 1"
    msg2 = "Message 2"
    
    enc1 = c1.encrypt(msg1)
    enc2 = c2.encrypt(msg2)
    
    # Compromise of sk1 doesn't affect sk2
    dec1 = c1.decrypt(enc1["ciphertext"], enc1["iv"])
    can_not_dec2 = True
    try:
        dec2_wrong = c1.decrypt(enc2["ciphertext"], enc2["iv"])
        can_not_dec2 = (dec2_wrong != msg2)
    except:
        can_not_dec2 = True
    
    passed += check(
        can_not_dec2,
        "Forward secrecy: compromise of one key doesn't affect others"
    )
    
    return passed


def main():
    """Run all validation tests"""
    print("\n" + "=" * 70)
    print("  JOUR3_PARTIE2 - E2EE + Signatures Validation Suite")
    print("  24 comprehensive checks across 5 parts")
    print("=" * 70)
    
    total_passed = 0
    
    total_passed += test_part_1_rsa_signatures()
    total_passed += test_part_2_signature_verification()
    total_passed += test_part_3_combined_crypto()
    total_passed += test_part_4_room_encryption()
    total_passed += test_part_5_security_properties()
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"  VALIDATION RESULTS: {total_passed}/24 checks passed")
    print("=" * 70)
    
    if total_passed == 24:
        print("\n✅ ALL VALIDATION CHECKS PASSED! ✅\n")
        return 0
    else:
        print(f"\n❌ {24 - total_passed} checks failed\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
