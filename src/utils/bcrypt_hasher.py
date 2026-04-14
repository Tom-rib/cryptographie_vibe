"""
Bcrypt hashing module for secure password management
Provides MD5-free password hashing with bcrypt
"""
import bcrypt


class BcryptHasher:
    """Secure password hashing using bcrypt with configurable cost factor"""
    
    def __init__(self, cost_factor=12):
        """
        Initialize BcryptHasher
        
        Args:
            cost_factor: bcrypt cost factor (10-12 recommended, higher = slower)
                        Each increment doubles computation time
                        12 = ~2^12 = 4096 iterations
        """
        if not 4 <= cost_factor <= 31:
            raise ValueError(f"Cost factor must be between 4 and 31, got {cost_factor}")
        self.cost_factor = cost_factor
    
    def hash(self, password):
        """
        Hash password using bcrypt
        
        Args:
            password (str): Plain text password to hash
            
        Returns:
            str: Bcrypt hash in format: $2b$cost$salt+digest
                 Salt is automatically generated (≥96 bits)
        """
        salt = bcrypt.gensalt(rounds=self.cost_factor)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode('utf-8')
    
    def verify(self, password, hashed):
        """
        Verify password against bcrypt hash (time-constant comparison)
        
        Args:
            password (str): Plain text password to verify
            hashed (str): Bcrypt hash to compare against
            
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception:
            # Handle invalid hash format
            return False
    
    def extract_components(self, bcrypt_hash):
        """
        Extract algorithm, cost factor, and salt from bcrypt hash
        
        Bcrypt format: $2b$cost$salt+digest
        Example: $2b$12$xt8pd3xiXXXXXXXXXXXXXXXXXXXXXXXX
        
        Args:
            bcrypt_hash (str): Full bcrypt hash
            
        Returns:
            dict: {
                'algo': 'bcrypt',
                'version': '2b',
                'cost': '12',
                'salt': 'xt8pd3xi...',  # First 22 chars are salt
                'digest': full hash
            }
        """
        parts = bcrypt_hash.split('$')
        if len(parts) < 4:
            return None
        
        return {
            'algo': 'bcrypt',
            'version': parts[1],
            'cost': parts[2],
            'salt': parts[3][:22],  # bcrypt salt is 22 chars
            'digest': bcrypt_hash
        }
    
    def needs_rehash(self, stored_hash, new_cost_factor=None):
        """
        Check if a stored hash needs to be rehashed
        (e.g., old MD5 format or outdated cost factor)
        
        Args:
            stored_hash (str): The stored hash to check
            new_cost_factor (int): Target cost factor (default: self.cost_factor)
            
        Returns:
            bool: True if rehashing is recommended
        """
        if new_cost_factor is None:
            new_cost_factor = self.cost_factor
        
        # Old MD5 format: base64 encoded, doesn't start with $2
        if not stored_hash.startswith('$2'):
            return True
        
        # Extract current cost
        try:
            components = self.extract_components(stored_hash)
            if components and int(components['cost']) < new_cost_factor:
                return True
        except (ValueError, TypeError):
            pass
        
        return False
