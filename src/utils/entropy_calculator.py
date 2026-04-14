"""
Password entropy calculator for Crypto Vibeness
Measures password strength based on entropy
"""
import math


class EntropyCalculator:
    """Calculate password entropy and strength"""

    @staticmethod
    def has_lowercase(password):
        """Check if password contains lowercase letters"""
        return any(c.islower() for c in password)

    @staticmethod
    def has_uppercase(password):
        """Check if password contains uppercase letters"""
        return any(c.isupper() for c in password)

    @staticmethod
    def has_digits(password):
        """Check if password contains digits"""
        return any(c.isdigit() for c in password)

    @staticmethod
    def has_special(password, special_chars="!@#$%^&*()-_=+[]{}|;:,.<>?"):
        """Check if password contains special characters"""
        return any(c in special_chars for c in password)

    @classmethod
    def calculate(cls, password, special_chars="!@#$%^&*()-_=+[]{}|;:,.<>?"):
        """
        Calculate password entropy and strength
        
        Returns:
            tuple: (entropy_bits, strength_label, strength_percentage)
        """
        if not password:
            return 0, "WEAK", 0

        # Calculate alphabet size
        alphabet_size = 0
        if cls.has_lowercase(password):
            alphabet_size += 26
        if cls.has_uppercase(password):
            alphabet_size += 26
        if cls.has_digits(password):
            alphabet_size += 10
        if cls.has_special(password, special_chars):
            alphabet_size += len(special_chars)

        # Calculate entropy: log2(alphabet_size ^ password_length)
        if alphabet_size > 0:
            entropy = math.log2(alphabet_size ** len(password))
        else:
            entropy = 0

        # Get strength label
        strength = cls.get_strength_label(entropy)

        # Calculate percentage (cap at 100%)
        percentage = min(int(entropy), 100)

        return entropy, strength, percentage

    @staticmethod
    def get_strength_label(entropy):
        """
        Get strength label based on entropy
        
        Categories:
        - < 40 bits: WEAK
        - 40-60 bits: MEDIUM
        - 60-80 bits: STRONG
        - > 80 bits: VERY STRONG
        """
        if entropy < 40:
            return "WEAK"
        elif entropy < 60:
            return "MEDIUM"
        elif entropy < 80:
            return "STRONG"
        else:
            return "VERY STRONG"

    @classmethod
    def format_strength(cls, password, special_chars="!@#$%^&*()-_=+[]{}|;:,.<>?"):
        """Format strength for display"""
        entropy, strength, percentage = cls.calculate(password, special_chars)
        return f"{percentage}% ({strength})"
