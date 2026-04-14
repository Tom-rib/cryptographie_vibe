"""
Password manager for Crypto Vibeness
Handles password hashing, validation, and storage
"""
import json
import os
import base64

# Handle import paths for both direct and relative imports
try:
    from utils.bcrypt_hasher import BcryptHasher
    from utils.key_derivation import KeyDerivation
except ImportError:
    try:
        from .bcrypt_hasher import BcryptHasher
        from .key_derivation import KeyDerivation
    except ImportError:
        # Fallback for test environments
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        from bcrypt_hasher import BcryptHasher
        from key_derivation import KeyDerivation


class PasswordManager:
    """Manage password hashing, validation, and storage"""

    def __init__(self, rules_file="data/password_rules.json", cost_factor=12):
        """Initialize password manager with rules and bcrypt hasher"""
        self.rules = self._load_rules(rules_file)
        self.special_chars = self._get_special_chars()
        self.hasher = BcryptHasher(cost_factor=cost_factor)

    @staticmethod
    def _load_rules(rules_file):
        """Load password rules from JSON file"""
        if not os.path.exists(rules_file):
            # Default rules
            return [
                {
                    "id": 1,
                    "name": "Minimum length",
                    "type": "length",
                    "min": 8,
                    "description": "At least 8 characters"
                },
                {
                    "id": 2,
                    "name": "Uppercase letters",
                    "type": "character_class",
                    "class": "uppercase",
                    "description": "At least 1 uppercase letter"
                },
                {
                    "id": 3,
                    "name": "Lowercase letters",
                    "type": "character_class",
                    "class": "lowercase",
                    "description": "At least 1 lowercase letter"
                },
                {
                    "id": 4,
                    "name": "Digits",
                    "type": "character_class",
                    "class": "digit",
                    "description": "At least 1 digit"
                }
            ]

        try:
            with open(rules_file, 'r') as f:
                data = json.load(f)
                # Handle both array format and object format with "rules" key
                if isinstance(data, list):
                    return data
                else:
                    return data.get("rules", [])
        except Exception as e:
            print(f"Error loading rules: {e}")
            return []

    def _get_special_chars(self):
        """Extract special characters from rules"""
        for rule in self.rules:
            if rule.get("class") == "special":
                return rule.get("special_chars", "!@#$%^&*()-_=+[]{}|;:,.<>?")
        return "!@#$%^&*()-_=+[]{}|;:,.<>?"

    def validate_password(self, password):
        """
        Validate password against rules
        
        Returns:
            tuple: (is_valid: bool, errors: list)
        """
        errors = []

        for rule in self.rules:
            if rule.get("type") == "length":
                min_len = rule.get("min", 8)
                if len(password) < min_len:
                    errors.append(rule.get("description", f"Password too short"))

            elif rule.get("type") == "character_class":
                char_class = rule.get("class", "")

                if char_class == "uppercase":
                    if not any(c.isupper() for c in password):
                        errors.append(rule.get("description", "Missing uppercase letter"))

                elif char_class == "lowercase":
                    if not any(c.islower() for c in password):
                        errors.append(rule.get("description", "Missing lowercase letter"))

                elif char_class == "digit":
                    if not any(c.isdigit() for c in password):
                        errors.append(rule.get("description", "Missing digit"))

                elif char_class == "special":
                    special = rule.get("special_chars", "!@#$%^&*()-_=+[]{}|;:,.<>?")
                    if not any(c in special for c in password):
                        errors.append(rule.get("description", "Missing special character"))

        return len(errors) == 0, errors

    def hash_password(self, password):
        """
        Hash password using bcrypt (replaces MD5)
        
        Args:
            password (str): Plain text password to hash
            
        Returns:
            str: Bcrypt hash with embedded salt
        """
        return self.hasher.hash(password)

    def verify_password(self, password, stored_hash):
        """
        Verify password against stored hash (time constant comparison)
        
        Args:
            password: User provided password
            stored_hash: Stored hash (bcrypt or old MD5 for migration)
            
        Returns:
            bool: True if password matches
        """
        # Handle old MD5 format for migration
        if not stored_hash.startswith('$2'):
            # Old MD5 format (base64 encoded)
            import hashlib
            import base64
            import hmac
            computed_hash = base64.b64encode(hashlib.md5(password.encode()).digest()).decode()
            return hmac.compare_digest(computed_hash, stored_hash)
        
        # New bcrypt format
        return self.hasher.verify(password, stored_hash)
    
    def needs_rehash(self, stored_hash):
        """
        Check if hash needs upgrading (e.g., from MD5 to bcrypt)
        
        Args:
            stored_hash (str): Hash to check
            
        Returns:
            bool: True if should be rehashed
        """
        return self.hasher.needs_rehash(stored_hash)

    @staticmethod
    def load_users(users_file="data/this_is_safe.txt"):
        """
        Load users from file (supports both old and new formats)
        
        Old format: username:base64_hash
        New format: username:bcrypt:cost:salt:digest
        
        Returns:
            dict: {username: hash_info_dict}
        """
        users = {}
        if not os.path.exists(users_file):
            return users

        try:
            with open(users_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split(':')
                    if len(parts) < 2:
                        continue
                    
                    username = parts[0]
                    
                    # New format: username:bcrypt:cost:salt:digest
                    if len(parts) >= 5 and parts[1] == 'bcrypt':
                        users[username] = {
                            'algo': 'bcrypt',
                            'cost': parts[2],
                            'salt': parts[3],
                            'hash': ':'.join(parts[4:])  # In case digest contains ':'
                        }
                    else:
                        # Old format: username:hash
                        users[username] = {
                            'algo': 'md5',
                            'hash': ':'.join(parts[1:])
                        }
        except Exception as e:
            print(f"Error loading users: {e}")

        return users

    @staticmethod
    def save_users(users, users_file="data/this_is_safe.txt"):
        """
        Save users to file in new format
        
        Format: username:bcrypt:cost:salt:digest
        
        Args:
            users: dict of {username: hash_str} or {username: hash_info_dict}
            users_file: path to users file
        """
        os.makedirs(os.path.dirname(users_file) or ".", exist_ok=True)
        try:
            with open(users_file, 'w') as f:
                for username, user_info in sorted(users.items()):
                    if isinstance(user_info, dict):
                        if user_info.get('algo') == 'bcrypt':
                            # New format
                            line = f"{username}:bcrypt:{user_info['cost']}:{user_info['salt']}:{user_info['hash']}\n"
                        else:
                            # Old MD5 format (shouldn't normally save this, but for migration)
                            line = f"{username}:{user_info['hash']}\n"
                    else:
                        # String hash - assume it's bcrypt
                        line = f"{username}:{user_info}\n"
                    f.write(line)
        except Exception as e:
            print(f"Error saving users: {e}")

    def add_user(self, username, password, users_file="data/this_is_safe.txt"):
        """
        Add or update a user with bcrypt hashing
        
        Args:
            username: User's username
            password: User's password
            users_file: path to users file
        """
        users = self.load_users(users_file)
        bcrypt_hash = self.hash_password(password)
        
        # Extract components for storage
        components = self.hasher.extract_components(bcrypt_hash)
        if components:
            users[username] = {
                'algo': 'bcrypt',
                'cost': components['cost'],
                'salt': components['salt'],
                'hash': bcrypt_hash
            }
        else:
            # Fallback: just store the hash
            users[username] = bcrypt_hash
        
        self.save_users(users, users_file)

    def add_user_from_hash(self, username, hash_str, users_file="data/this_is_safe.txt"):
        """
        Add user with a pre-existing hash (for migration)
        """
        users = self.load_users(users_file)
        
        if hash_str.startswith('$2'):
            # Bcrypt format
            components = self.hasher.extract_components(hash_str)
            if components:
                users[username] = {
                    'algo': 'bcrypt',
                    'cost': components['cost'],
                    'salt': components['salt'],
                    'hash': hash_str
                }
            else:
                users[username] = hash_str
        else:
            # Old format or unknown
            users[username] = {
                'algo': 'md5',
                'hash': hash_str
            }
        
        self.save_users(users, users_file)

    @staticmethod
    def user_exists(username, users_file="data/this_is_safe.txt"):
        """Check if user exists"""
        users = PasswordManager.load_users(users_file)
        return username in users

    @staticmethod
    def get_user_hash(username, users_file="data/this_is_safe.txt"):
        """
        Get hash for a user (handles both old and new formats)
        
        Returns:
            str or dict: Hash string or user info dict
        """
        users = PasswordManager.load_users(users_file)
        user_info = users.get(username)
        
        # If it's a dict, return just the hash for verify operations
        if isinstance(user_info, dict):
            return user_info.get('hash', user_info)
        
        return user_info

    # ===========================
    # Key Derivation and Storage (for symmetric encryption)
    # ===========================

    @staticmethod
    def derive_key(password):
        """
        Derive a 256-bit encryption key from a password using PBKDF2.
        
        Args:
            password (str): User's password
        
        Returns:
            tuple: (key_bytes, salt_bytes, salt_b64)
        """
        key, salt = KeyDerivation.derive(password)
        salt_b64 = base64.b64encode(salt).decode('ascii')
        return key, salt, salt_b64

    @staticmethod
    def save_user_key(username, password, keys_file="data/user_keys_do_not_steal_plz.txt"):
        """
        Derive a key from password and save it (username:algo:iterations:salt_b64:key_b64).
        
        Args:
            username (str): Username
            password (str): Password to derive from
            keys_file (str): Path to key storage file
        
        Returns:
            tuple: (key_bytes, salt_b64) for later use
        """
        key, salt, salt_b64 = PasswordManager.derive_key(password)
        key_b64 = base64.b64encode(key).decode('ascii')
        
        # Load existing keys
        keys = PasswordManager.load_user_keys(keys_file)
        
        # Save new key in format: username:pbkdf2:100000:salt_b64:key_b64
        keys[username] = {
            'algo': 'pbkdf2',
            'iterations': KeyDerivation.ITERATIONS,
            'salt_b64': salt_b64,
            'key_b64': key_b64
        }
        
        # Write to file
        os.makedirs(os.path.dirname(keys_file) or '.', exist_ok=True)
        with open(keys_file, 'w') as f:
            for user, info in sorted(keys.items()):
                line = f"{user}:pbkdf2:{info['iterations']}:{info['salt_b64']}:{info['key_b64']}\n"
                f.write(line)
        
        return key, salt_b64

    @staticmethod
    def load_user_keys(keys_file="data/user_keys_do_not_steal_plz.txt"):
        """
        Load user keys from file.
        
        Format: username:algo:iterations:salt_b64:key_b64
        
        Returns:
            dict: {username: {algo, iterations, salt_b64, key_b64}}
        """
        keys = {}
        
        if not os.path.exists(keys_file):
            return keys
        
        try:
            with open(keys_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split(':')
                    if len(parts) >= 5:
                        username = parts[0]
                        algo = parts[1]
                        iterations = int(parts[2])
                        salt_b64 = parts[3]
                        key_b64 = parts[4]
                        
                        keys[username] = {
                            'algo': algo,
                            'iterations': iterations,
                            'salt_b64': salt_b64,
                            'key_b64': key_b64
                        }
        except Exception as e:
            print(f"Warning: Failed to load keys: {e}")
        
        return keys

    @staticmethod
    def get_user_key(username, keys_file="data/user_keys_do_not_steal_plz.txt"):
        """
        Get the encryption key for a user (in bytes, not base64).
        
        Args:
            username (str): Username
            keys_file (str): Path to key storage file
        
        Returns:
            bytes: 32-byte encryption key, or None if not found
        """
        keys = PasswordManager.load_user_keys(keys_file)
        user_key = keys.get(username)
        
        if user_key:
            key_b64 = user_key.get('key_b64')
            if key_b64:
                return base64.b64decode(key_b64)
        
        return None

    @staticmethod
    def get_user_salt_b64(username, keys_file="data/user_keys_do_not_steal_plz.txt"):
        """
        Get the salt for a user (base64-encoded).
        Used to re-derive the key during login.
        
        Args:
            username (str): Username
            keys_file (str): Path to key storage file
        
        Returns:
            str: Base64-encoded salt, or None if not found
        """
        keys = PasswordManager.load_user_keys(keys_file)
        user_key = keys.get(username)
        
        if user_key:
            return user_key.get('salt_b64')
        
        return None
