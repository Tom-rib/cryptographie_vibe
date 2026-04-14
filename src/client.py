"""
Crypto Vibeness Client - IRC-like chat system
Day 2 Part 2: Symmetric encryption (AES-256-CBC)
"""
import socket
import json
import threading
import sys
import os
import time
import base64

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Try to import crypto modules
try:
    from utils.crypto import AES256Cipher
    from utils.key_derivation import KeyDerivation
    CRYPTO_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Crypto modules not available: {e}")
    CRYPTO_AVAILABLE = False


class ChatClient:
    """Client for connecting to Crypto Vibeness chat server"""

    def __init__(self, host="localhost", port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.username = None
        self.running = False
        self.username_requested = False
        self.authenticated = False
        self.awaiting_password_input = False
        
        # Encryption key management
        self.encryption_key = None
        self.cipher = None
        self.local_key_dir = None

    def _setup_encryption_from_password(self, password, salt_b64=None):
        """
        Derive encryption key from password and setup cipher.
        
        Args:
            password (str): User's password
            salt_b64 (str): Optional base64-encoded salt (for re-derivation on login)
        """
        if not CRYPTO_AVAILABLE:
            return
        
        try:
            if salt_b64:
                # Login scenario: use provided salt to re-derive same key
                key = KeyDerivation.derive_with_salt(password, salt_b64)
            else:
                # Signup scenario: derive new key and salt
                key, salt = KeyDerivation.derive(password)
                salt_b64 = base64.b64encode(salt).decode('ascii')
                
                # Save key locally for future use
                self._save_key_locally(key, salt_b64)
            
            # Create cipher for this session
            self.encryption_key = key
            self.cipher = AES256Cipher(key)
            print(f"🔐 Encryption key derived from password")
            
        except Exception as e:
            print(f"⚠️  Warning: Failed to setup encryption: {e}")
    
    def _save_key_locally(self, key, salt_b64):
        """
        Save encryption key to local storage (~/.crypto-vibeness/username/key.txt).
        
        Args:
            key (bytes): 32-byte encryption key
            salt_b64 (str): Base64-encoded salt for re-derivation
        """
        if not self.username:
            return
        
        try:
            # Create directory
            key_dir = os.path.expanduser(f"~/.crypto-vibeness/{self.username}")
            os.makedirs(key_dir, exist_ok=True)
            self.local_key_dir = key_dir
            
            # Save key and salt
            key_file = os.path.join(key_dir, "key.txt")
            with open(key_file, 'w') as f:
                # Format: key_b64:salt_b64
                key_b64 = base64.b64encode(key).decode('ascii')
                f.write(f"{key_b64}:{salt_b64}\n")
            
            os.chmod(key_file, 0o600)  # Make readable only by user
            print(f"💾 Key saved to {key_file}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not save key locally: {e}")

    def connect(self):
        """Connect to server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"✓ Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False

    def send_message(self, msg_dict):
        """Send JSON message to server"""
        try:
            msg = json.dumps(msg_dict) + "\n"
            self.socket.sendall(msg.encode('utf-8'))
        except Exception as e:
            print(f"✗ Send error: {e}")
            self.running = False

    def receive_loop(self):
        """Continuously receive messages from server"""
        buffer = ""
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    self.running = False
                    print("\n✗ Disconnected from server")
                    break

                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line:
                        msg = json.loads(line)
                        self.handle_message(msg)

            except Exception as e:
                if self.running:
                    print(f"✗ Receive error: {e}")
                self.running = False
                break

    def handle_message(self, msg):
        """Handle received message"""
        msg_type = msg.get("type", "")

        if msg_type == "username_request":
            self.username_requested = True

        elif msg_type == "welcome":
            self.authenticated = True
            print(f"\n{msg.get('content')}\n")

        elif msg_type == "auth":
            # Authentication prompt - need password or action
            action = msg.get("action", "")
            content = msg.get("content", "")
            print(f"\n→ {content}")
            self.awaiting_password_input = True

        elif msg_type == "auth_success":
            self.authenticated = True
            print(f"\n✅ {msg.get('content')}\n")
            self.awaiting_password_input = False
            
            # Handle encryption key setup (for JOUR2_PARTIE2)
            # Server may include salt_b64 for re-deriving key on login
            if CRYPTO_AVAILABLE and "salt_b64" in msg:
                # This is a login with existing user - re-derive key
                if hasattr(self, '_last_password'):
                    self._setup_encryption_from_password(self._last_password, msg.get("salt_b64"))
                    delattr(self, '_last_password')

        elif msg_type == "auth_error":
            print(f"\n⚠️  {msg.get('content')}")
            self.awaiting_password_input = True

        elif msg_type == "auth_info":
            print(f"\n→ {msg.get('content')}")
            self.awaiting_password_input = True

        elif msg_type == "message":
            color = msg.get("color", "")
            reset = "\u001b[0m"
            timestamp = msg.get("timestamp", "")
            from_user = msg.get("from", "")
            
            # Try to decrypt if message is encrypted (JOUR2_PARTIE2)
            if CRYPTO_AVAILABLE and self.cipher and "encrypted_content" in msg:
                try:
                    content = self.cipher.decrypt(msg.get("encrypted_content"), msg.get("iv"))
                except Exception as e:
                    content = f"[Decryption failed: {e}]"
            else:
                # Fallback to plaintext (for backward compatibility)
                content = msg.get("content", "")

            print(f"{color}[{timestamp}] {from_user}{reset}: {content}")

        elif msg_type == "system":
            print(f"\n→ {msg.get('content')}\n")

        elif msg_type == "error":
            print(f"\n✗ Error: {msg.get('content')}\n")

        elif msg_type == "rooms":
            print("\n📌 Available rooms:")
            for room in msg.get("content", []):
                print(f"  - {room}")
            print()

        elif msg_type == "users":
            print("\n👥 Connected users:")
            for user in msg.get("content", []):
                print(f"  - {user}")
            print()

        elif msg_type == "help":
            print("\n❓ Commands:")
            for cmd in msg.get("content", []):
                print(f"  {cmd}")
            print()

    def request_username(self):
        """Request username from user"""
        username = input("Choose username: ").strip()
        self.username = username
        self.send_message({"username": username})

    def send_loop(self):
        """Continuously read user input and send to server"""
        while self.running:
            try:
                # Wait for username request
                if self.username_requested and self.username is None:
                    self.request_username()
                    self.username_requested = False

                # Wait for password during authentication
                if self.awaiting_password_input:
                    user_input = input()
                    if not user_input:
                        continue
                    
                    # Store password for key derivation (JOUR2_PARTIE2)
                    if CRYPTO_AVAILABLE:
                        self._last_password = user_input
                        # For new signup, derive key immediately
                        self._setup_encryption_from_password(user_input)
                    
                    self.send_message({"password": user_input})
                    self.awaiting_password_input = False
                    continue

                # Normal chat input (only after authentication)
                if not self.authenticated:
                    continue

                user_input = input()
                if not user_input:
                    continue

                if user_input.startswith("/"):
                    # Command
                    parts = user_input.split()
                    cmd = parts[0][1:]  # Remove /
                    args = parts[1:]
                    
                    if cmd == "quit":
                        self.running = False
                        break
                    
                    self.send_message({
                        "type": "command",
                        "command": cmd,
                        "args": args
                    })
                else:
                    # Regular message - encrypt if cipher is available
                    msg_dict = {
                        "type": "message",
                    }
                    
                    if CRYPTO_AVAILABLE and self.cipher:
                        # Encrypt the message (JOUR2_PARTIE2)
                        try:
                            encrypted = self.cipher.encrypt(user_input)
                            msg_dict["encrypted_content"] = encrypted["ciphertext"]
                            msg_dict["iv"] = encrypted["iv"]
                        except Exception as e:
                            print(f"✗ Encryption error: {e}")
                            continue
                    else:
                        # Fallback to plaintext
                        msg_dict["content"] = user_input
                    
                    self.send_message(msg_dict)

            except EOFError:
                self.running = False
                break
            except Exception as e:
                print(f"✗ Send error: {e}")
                self.running = False

    def run(self):
        """Main client loop"""
        if not self.connect():
            return

        self.running = True

        # Start receive thread
        receive_thread = threading.Thread(target=self.receive_loop)
        receive_thread.daemon = False
        receive_thread.start()

        # Start send thread
        send_thread = threading.Thread(target=self.send_loop)
        send_thread.daemon = False
        send_thread.start()

        # Wait for threads to finish
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
            print("\n✓ Goodbye!")

        # Wait for threads to exit
        receive_thread.join(timeout=1)
        send_thread.join(timeout=1)

        # Close socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Crypto Vibeness Chat Client")
    parser.add_argument("--host", default="localhost", help="Server host (default: localhost)")
    parser.add_argument("--port", type=int, default=5555, help="Server port (default: 5555)")

    args = parser.parse_args()

    client = ChatClient(args.host, args.port)
    client.run()


if __name__ == "__main__":
    main()
