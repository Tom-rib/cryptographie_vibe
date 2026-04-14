"""
Password manager for Crypto Vibeness
Handles password hashing, validation, and storage
"""
import hashlib
import base64
import hmac
import json
import os


class PasswordManager:
    """Manage password hashing, validation, and storage"""

    def __init__(self, rules_file="data/password_rules.json"):
        """Initialize password manager with rules"""
        self.rules = self._load_rules(rules_file)
        self.special_chars = self._get_special_chars()

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

    @staticmethod
    def hash_password(password):
        """
        Hash password using MD5 and encode in base64
        
        Returns:
            str: Base64 encoded MD5 hash
        """
        md5_hash = hashlib.md5(password.encode()).digest()
        base64_encoded = base64.b64encode(md5_hash).decode()
        return base64_encoded

    @staticmethod
    def verify_password(password, stored_hash):
        """
        Verify password against stored hash (time constant comparison)
        
        Args:
            password: User provided password
            stored_hash: Stored hash in base64
            
        Returns:
            bool: True if password matches
        """
        computed_hash = PasswordManager.hash_password(password)
        return hmac.compare_digest(computed_hash, stored_hash)

    @staticmethod
    def load_users(users_file="data/this_is_safe.txt"):
        """
        Load users from file
        
        Returns:
            dict: {username: hash}
        """
        users = {}
        if not os.path.exists(users_file):
            return users

        try:
            with open(users_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue
                    username, password_hash = line.split(':', 1)
                    users[username] = password_hash
        except Exception as e:
            print(f"Error loading users: {e}")

        return users

    @staticmethod
    def save_users(users, users_file="data/this_is_safe.txt"):
        """
        Save users to file
        
        Args:
            users: dict {username: hash}
            users_file: path to users file
        """
        os.makedirs(os.path.dirname(users_file) or ".", exist_ok=True)
        try:
            with open(users_file, 'w') as f:
                for username, password_hash in sorted(users.items()):
                    f.write(f"{username}:{password_hash}\n")
        except Exception as e:
            print(f"Error saving users: {e}")

    @staticmethod
    def add_user(username, password, users_file="data/this_is_safe.txt"):
        """
        Add or update a user
        
        Args:
            username: User's username
            password: User's password
            users_file: path to users file
        """
        users = PasswordManager.load_users(users_file)
        users[username] = PasswordManager.hash_password(password)
        PasswordManager.save_users(users, users_file)

    @staticmethod
    def user_exists(username, users_file="data/this_is_safe.txt"):
        """Check if user exists"""
        users = PasswordManager.load_users(users_file)
        return username in users

    @staticmethod
    def get_user_hash(username, users_file="data/this_is_safe.txt"):
        """Get hash for a user"""
        users = PasswordManager.load_users(users_file)
        return users.get(username)
