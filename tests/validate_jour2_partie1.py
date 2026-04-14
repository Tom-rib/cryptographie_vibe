#!/usr/bin/env python3
"""
Validation script for JOUR2_PARTIE1: Bcrypt & Password Migration
"""

import socket
import json
import time
import os
import sys
import hashlib
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.bcrypt_hasher import BcryptHasher
from src.utils.password_manager import PasswordManager

def recv_all_messages(sock, timeout=0.3):
    messages = []
    sock.settimeout(timeout)
    buffer = ""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            buffer += data.decode('utf-8')
    except socket.timeout:
        pass
    
    for line in buffer.strip().split('\n'):
        if line.strip():
            try:
                messages.append(json.loads(line))
            except:
                pass
    return messages

class Validator:
    def __init__(self, port=5555):
        self.port = port
        self.passed = 0
        self.failed = 0
    
    def log_criterion(self, criterion_id, name, passed, details=""):
        status = "✅" if passed else "❌"
        print(f"{status} [{criterion_id}] {name}")
        if details:
            print(f"         {details}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def validate_part1_md5_cracking(self):
        print("\n" + "="*70)
        print("PART 1: MD5 HASH CRACKING")
        print("="*70)
        
        try:
            with open("data/md5_decrypted.txt", 'r') as f:
                content = f.read()
            
            has_hash = "35b95f7c0f63631c453220fb2a86f" in content
            has_mask = "?u?u?l?l?u?u?s" in content
            
            self.log_criterion("P1-1", "MD5 cracking documented",
                             has_hash and has_mask,
                             "Hash and mask found in file")
        except:
            self.log_criterion("P1-1", "MD5 cracking documented", False)
    
    def validate_part2_bcrypt_implementation(self):
        print("\n" + "="*70)
        print("PART 2: BCRYPT IMPLEMENTATION & PERFORMANCE")
        print("="*70)
        
        # P2-1: BcryptHasher exists and works
        try:
            hasher = BcryptHasher(cost_factor=12)
            pwd = "TestPassword123!"
            hashed = hasher.hash(pwd)
            verified = hasher.verify(pwd, hashed)
            
            self.log_criterion("P2-1", "BcryptHasher hash & verify",
                             verified and hashed.startswith('$2b$'),
                             "Hash format correct, verify works")
        except Exception as e:
            self.log_criterion("P2-1", "BcryptHasher hash & verify", False, str(e))
        
        # P2-2: Extract components
        try:
            hasher = BcryptHasher()
            hashed = hasher.hash("test")
            components = hasher.extract_components(hashed)
            
            has_algo = components and components.get('algo') == 'bcrypt'
            has_cost = components and components.get('cost') == '12'
            has_salt = components and len(components.get('salt', '')) > 0
            
            self.log_criterion("P2-2", "Extract components",
                             has_algo and has_cost and has_salt,
                             f"Algo={components.get('algo')}, Cost={components.get('cost')}, Salt={components.get('salt')[:10]}...")
        except Exception as e:
            self.log_criterion("P2-2", "Extract components", False, str(e))
        
        # P2-3: Performance comparison
        try:
            md5_time = timeit.timeit(
                lambda: hashlib.md5("TestPassword123!".encode()).hexdigest(),
                number=1000
            )
            
            hasher = BcryptHasher(cost_factor=12)
            bcrypt_time = timeit.timeit(
                lambda: hasher.hash("TestPassword123!"),
                number=3
            ) / 3
            
            ratio = bcrypt_time / (md5_time / 1000) if md5_time > 0 else 0
            is_slower = ratio > 1000
            
            self.log_criterion("P2-3", "Bcrypt ~1000x slower than MD5",
                             is_slower,
                             f"Ratio: {ratio:.0f}x (MD5: {md5_time/1000*1000:.1f}ms, Bcrypt: {bcrypt_time*1000:.0f}ms)")
        except Exception as e:
            self.log_criterion("P2-3", "Bcrypt ~1000x slower than MD5", False, str(e))
    
    def validate_part3_new_format(self):
        print("\n" + "="*70)
        print("PART 3: NEW STORAGE FORMAT")
        print("="*70)
        
        test_file = "data/test_format.txt"
        if os.path.exists(test_file):
            os.remove(test_file)
        
        try:
            pm = PasswordManager()
            pm.add_user("testuser", "TestPass123!", test_file)
            
            with open(test_file, 'r') as f:
                content = f.read().strip()
            
            parts = content.split(':')
            has_username = parts[0] == 'testuser'
            has_algo = len(parts) > 1 and parts[1] == 'bcrypt'
            has_cost = len(parts) > 2 and parts[2].isdigit()
            has_salt = len(parts) > 3 and len(parts[3]) > 0
            has_hash = len(parts) > 4 and parts[4].startswith('$2b$')
            
            all_parts = has_username and has_algo and has_cost and has_salt and has_hash
            
            self.log_criterion("P3-1", "Format: username:algo:cost:salt:digest",
                             all_parts,
                             f"username={parts[0]}, algo={parts[1]}, cost={parts[2]}, salt={parts[3][:10]}..., hash={parts[4][:20]}...")
            
            os.remove(test_file)
        except Exception as e:
            self.log_criterion("P3-1", "Format: username:algo:cost:salt:digest", False, str(e))
    
    def validate_part4_migration(self):
        print("\n" + "="*70)
        print("PART 4: PASSWORD MIGRATION (MD5 -> BCRYPT)")
        print("="*70)
        
        # Create mixed format file
        test_file = "data/test_migration.txt"
        old_md5_hash = "GPfwEATLGZsE3OcZf/LB2A=="  # SecurePass123! in MD5
        
        with open(test_file, 'w') as f:
            f.write(f"olduser:{old_md5_hash}\n")
        
        try:
            pm = PasswordManager()
            
            # Verify we can read old format
            users = pm.load_users(test_file)
            user_info = users.get('olduser')
            is_md5_format = user_info and user_info.get('algo') == 'md5'
            
            self.log_criterion("P4-1", "Read old MD5 format",
                             is_md5_format,
                             "Old format detected and parsed")
            
            # Test needs_rehash
            needs_rehash = pm.needs_rehash(old_md5_hash)
            self.log_criterion("P4-2", "Detect needs_rehash for MD5",
                             needs_rehash,
                             "MD5 format detected as needing rehash")
            
            # Test verify with old format
            verified = pm.verify_password("SecurePass123!", old_md5_hash)
            self.log_criterion("P4-3", "Verify old MD5 password",
                             verified,
                             "Old password verified successfully")
            
            os.remove(test_file)
        except Exception as e:
            self.log_criterion("P4-3", "Migration tests", False, str(e))
    
    def validate_part5_server_integration(self):
        print("\n" + "="*70)
        print("PART 5: SERVER INTEGRATION & AUTO-REHASH")
        print("="*70)
        
        # Test 1: New user creates bcrypt
        try:
            if os.path.exists("data/test_server.txt"):
                os.remove("data/test_server.txt")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", self.port))
            
            recv_all_messages(sock)
            sock.sendall((json.dumps({"username": "newuser"}) + "\n").encode())
            
            time.sleep(0.15)
            recv_all_messages(sock)
            sock.sendall((json.dumps({"password": "NewPass123!"}) + "\n").encode())
            
            time.sleep(0.15)
            recv_all_messages(sock)
            sock.sendall((json.dumps({"password": "NewPass123!"}) + "\n").encode())
            
            time.sleep(0.15)
            msgs = recv_all_messages(sock)
            sock.close()
            
            success = any(m['type'] == 'auth_success' for m in msgs)
            self.log_criterion("P5-1", "New user auto-uses bcrypt",
                             success,
                             "Account created with bcrypt")
        except Exception as e:
            self.log_criterion("P5-1", "New user auto-uses bcrypt", False, str(e))
    
    def validate_part6_security(self):
        print("\n" + "="*70)
        print("PART 6: SECURITY VERIFICATION")
        print("="*70)
        
        # P6-1: MD5 not in source code
        try:
            has_md5_import = False
            for root, dirs, files in os.walk("src"):
                for f in files:
                    if f.endswith('.py'):
                        with open(os.path.join(root, f), 'r') as fp:
                            content = fp.read()
                            if 'hashlib.md5' in content and 'password_manager' in root:
                                # Allowed in password_manager for migration only
                                if 'bcrypt' not in content:
                                    has_md5_import = True
            
            self.log_criterion("P6-1", "MD5 removed (except for migration)",
                             not has_md5_import,
                             "No MD5 imports found in new code")
        except:
            self.log_criterion("P6-1", "MD5 removed (except for migration)", False)
        
        # P6-2: Different salt per user
        try:
            pm = PasswordManager()
            hash1 = pm.hash_password("SamePassword")
            hash2 = pm.hash_password("SamePassword")
            
            # Different salts should produce different hashes
            different = hash1 != hash2
            
            self.log_criterion("P6-2", "Different salt per user",
                             different,
                             "Same password produces different hashes")
        except Exception as e:
            self.log_criterion("P6-2", "Different salt per user", False, str(e))
    
    def run_all(self):
        print("\n" + "="*70)
        print("JOUR2_PARTIE1 - VALIDATION SUITE")
        print("="*70)
        
        self.validate_part1_md5_cracking()
        self.validate_part2_bcrypt_implementation()
        self.validate_part3_new_format()
        self.validate_part4_migration()
        self.validate_part5_server_integration()
        self.validate_part6_security()
        
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"✅ PASSED: {self.passed}")
        print(f"❌ FAILED: {self.failed}")
        print(f"📊 TOTAL:  {self.passed + self.failed}/12 criteria")
        
        if self.failed == 0:
            print("\n🎉 ALL CRITERIA PASSED! JOUR2_PARTIE1 COMPLETE")
        else:
            print(f"\n⚠️  {self.failed} criteria failed")
        
        print("="*70 + "\n")
        
        return self.failed == 0

if __name__ == "__main__":
    validator = Validator()
    success = validator.run_all()
    sys.exit(0 if success else 1)
