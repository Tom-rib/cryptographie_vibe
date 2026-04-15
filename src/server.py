"""
Crypto Vibeness Server - IRC-like chat system
Day 1 Part 2: Authentication with MD5
"""
import socket
import json
import threading
import hashlib
import os
import sys
import base64
from datetime import datetime
from pathlib import Path

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
from utils.logger import CryptoLogger
from utils.password_manager import PasswordManager
from utils.entropy_calculator import EntropyCalculator
from utils.asymmetric_crypto import RSACrypto
from utils.signature import RSASignature


class Room:
    """Represents a chat room"""

    def __init__(self, name, password=None):
        self.name = name
        self.password = password
        self.clients = {}  # {username: socket}
        self.lock = threading.Lock()

    def add_client(self, username, client_socket):
        """Add client to room"""
        with self.lock:
            self.clients[username] = client_socket

    def remove_client(self, username):
        """Remove client from room"""
        with self.lock:
            if username in self.clients:
                del self.clients[username]

    def get_clients(self):
        """Get all client sockets except the requester"""
        with self.lock:
            return dict(self.clients)

    def is_protected(self):
        """Check if room is password protected"""
        return self.password is not None

    def check_password(self, password):
        """Verify room password"""
        return self.password == password


class RoomManager:
    """Manages all chat rooms"""

    def __init__(self):
        self.rooms = {"general": Room("general")}
        self.lock = threading.Lock()
        
        # Room encryption keys (JOUR3_PARTIE2)
        # Format: {room_name: 32-byte encryption key}
        self.room_keys = {}
        self.room_keys_lock = threading.Lock()
        
        # Generate key for general room
        self._generate_room_key("general")

    def create_room(self, name, password=None):
        """Create a new room"""
        with self.lock:
            if name not in self.rooms:
                self.rooms[name] = Room(name, password)
                # Generate encryption key for new room (JOUR3_PARTIE2)
                self._generate_room_key(name)
                return True
            return False
    
    def _generate_room_key(self, room_name):
        """Generate and store encryption key for a room (JOUR3_PARTIE2)"""
        with self.room_keys_lock:
            if room_name not in self.room_keys:
                # Generate 256-bit (32-byte) room key
                self.room_keys[room_name] = os.urandom(32)
    
    def get_room_key(self, room_name):
        """Get room encryption key (JOUR3_PARTIE2)"""
        with self.room_keys_lock:
            return self.room_keys.get(room_name)

    def get_room(self, name):
        """Get room by name"""
        with self.lock:
            return self.rooms.get(name)

    def join_room(self, room_name, username, client_socket, password=None):
        """Add client to room"""
        with self.lock:
            if room_name not in self.rooms:
                return False, "Room does not exist"

            room = self.rooms[room_name]
            if room.is_protected() and room.password != password:
                return False, "Wrong password"

            room.add_client(username, client_socket)
            return True, "Joined room"

    def leave_room(self, room_name, username):
        """Remove client from room"""
        with self.lock:
            if room_name in self.rooms:
                self.rooms[room_name].remove_client(username)

    def list_rooms(self):
        """List all rooms"""
        with self.lock:
            return list(self.rooms.keys())

    def get_room_info(self):
        """Get info about all rooms"""
        with self.lock:
            info = {}
            for name, room in self.rooms.items():
                info[name] = {
                    "protected": room.is_protected(),
                    "clients": list(room.clients.keys())
                }
            return info


class ClientHandler(threading.Thread):
    """Handle individual client connections"""

    def __init__(self, client_socket, client_address, room_manager, all_users, logger, colors_config, public_key_registry=None, registry_lock=None):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.room_manager = room_manager
        self.all_users = all_users
        self.logger = logger
        self.colors_config = colors_config
        self.username = None
        self.current_room = "general"
        self.daemon = True
        
        # Public key registry (JOUR3_PARTIE1)
        self.public_key_registry = public_key_registry or {}
        self.registry_lock = registry_lock or threading.Lock()

    def send_message(self, msg_dict):
        """Send JSON message to client"""
        try:
            msg = json.dumps(msg_dict) + "\n"
            self.client_socket.sendall(msg.encode('utf-8'))
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")

    def receive_message(self):
        """Receive JSON message from client"""
        try:
            buffer = ""
            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    return None
                buffer += data.decode('utf-8')
                if '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    return json.loads(line)
        except Exception as e:
            self.logger.error(f"Failed to receive message: {e}")
            return None

    def get_user_color(self, username):
        """Get deterministic color for username"""
        hash_val = int(hashlib.md5(username.encode()).hexdigest(), 16)
        color_idx = hash_val % len(self.colors_config["colors"])
        return self.colors_config["colors"][str(color_idx)]

    def broadcast_to_room(self, message_dict, exclude_sender=False):
        """Broadcast message to all clients in current room"""
        room = self.room_manager.get_room(self.current_room)
        if not room:
            return

        clients = room.get_clients()
        for username, client_socket in clients.items():
            if exclude_sender and username == self.username:
                continue
            try:
                msg = json.dumps(message_dict) + "\n"
                client_socket.sendall(msg.encode('utf-8'))
            except Exception as e:
                self.logger.error(f"Failed to broadcast to {username}: {e}")

    def handle_command(self, command_data):
        """Handle client commands"""
        cmd = command_data.get("command", "")
        args = command_data.get("args", [])

        if cmd == "join":
            self.handle_join(args)
        elif cmd == "create":
            self.handle_create(args)
        elif cmd == "rooms":
            self.handle_list_rooms()
        elif cmd == "users":
            self.handle_list_users()
        elif cmd == "help":
            self.handle_help()
        elif cmd == "quit":
            return False  # Signal to disconnect
        else:
            self.send_message({
                "type": "error",
                "content": f"Unknown command: {cmd}"
            })

        return True

    def handle_join(self, args):
        """Handle /join command"""
        if not args:
            self.send_message({"type": "error", "content": "Usage: /join <room_name> [password]"})
            return

        room_name = args[0]
        password = args[1] if len(args) > 1 else None

        # Leave current room
        self.room_manager.leave_room(self.current_room, self.username)

        # Try to join new room
        success, message = self.room_manager.join_room(room_name, self.username, self.client_socket, password)

        if success:
            self.current_room = room_name
            self.logger.log("JOIN_ROOM", self.username, room_name)
            self.send_message({"type": "system", "content": f"Joined room: {room_name}"})
            
            # Send room encryption key to client (JOUR2_PARTIE2)
            room_key = self.room_manager.get_room_key(room_name)
            if room_key:
                room_key_b64 = base64.b64encode(room_key).decode('ascii')
                self.send_message({
                    "type": "room_key",
                    "room": room_name,
                    "key_b64": room_key_b64
                })
            
            # Notify others in room
            self.broadcast_to_room({
                "type": "system",
                "content": f"{self.username} joined the room"
            }, exclude_sender=True)
        else:
            # Rejoin previous room
            self.room_manager.join_room(self.current_room, self.username, self.client_socket)
            self.send_message({"type": "error", "content": message})

    def handle_create(self, args):
        """Handle /create command"""
        if not args:
            self.send_message({"type": "error", "content": "Usage: /create <room_name> [password]"})
            return

        room_name = args[0]
        password = args[1] if len(args) > 1 else None

        if self.room_manager.create_room(room_name, password):
            self.logger.log("CREATE_ROOM", self.username, f"{room_name} (protected={password is not None})")
            self.send_message({"type": "system", "content": f"Room created: {room_name}"})
        else:
            self.send_message({"type": "error", "content": f"Room {room_name} already exists"})

    def handle_list_rooms(self):
        """Handle /rooms command"""
        info = self.room_manager.get_room_info()
        rooms_list = []
        for name, data in info.items():
            protected = "[PROTECTED]" if data["protected"] else ""
            current = " (*)" if name == self.current_room else ""
            rooms_list.append(f"{name} {protected}{current}")

        self.send_message({
            "type": "rooms",
            "content": rooms_list
        })

    def handle_list_users(self):
        """Handle /users command"""
        info = self.room_manager.get_room_info()
        users = []
        for name, data in info.items():
            for username in data["clients"]:
                if username not in users:
                    users.append(username)

        self.send_message({
            "type": "users",
            "content": users
        })

    def handle_help(self):
        """Handle /help command"""
        help_text = [
            "/help - Show this help",
            "/rooms - List all rooms",
            "/join <room> [password] - Join a room",
            "/create <room> [password] - Create a room",
            "/users - List all connected users",
            "/quit - Disconnect"
        ]
        self.send_message({"type": "help", "content": help_text})

    def _authenticate_user(self, username, password_manager):
        """
        Authenticate user (create account or login)
        
        Returns:
            bool: True if authentication successful
        """
        # Check if user exists
        user_exists = password_manager.user_exists(username)

        if user_exists:
            # Existing user - ask for password
            return self._login_existing_user(username, password_manager)
        else:
            # New user - create account
            return self._create_new_account(username, password_manager)

    def _login_existing_user(self, username, password_manager):
        """Handle login for existing user with auto-rehash on login"""
        self.send_message({
            "type": "auth",
            "action": "login",
            "content": "Username exists. Enter password:"
        })

        max_attempts = 3
        for attempt in range(max_attempts):
            password_data = self.receive_message()
            if not password_data or "password" not in password_data:
                return False

            password = password_data["password"]
            stored_hash = password_manager.get_user_hash(username)

            if password_manager.verify_password(password, stored_hash):
                # Get user's encryption key salt for client to re-derive key on login
                salt_b64 = PasswordManager.get_user_salt_b64(username)
                
                auth_success_msg = {
                    "type": "auth_success",
                    "content": f"Authentication successful! Welcome back {username}!"
                }
                
                # Include salt if available (allows client to re-derive encryption key)
                if salt_b64:
                    auth_success_msg["salt_b64"] = salt_b64
                
                self.send_message(auth_success_msg)
                
                # Check if password needs rehashing (e.g., from MD5 to bcrypt)
                if password_manager.needs_rehash(stored_hash):
                    self.logger.log("AUTH_REHASH", username, "Upgrading password to bcrypt")
                    # Rehash and save
                    password_manager.add_user(username, password)
                    self.send_message({
                        "type": "auth_info",
                        "content": "[Server: Password upgraded to bcrypt]"
                    })
                
                self.logger.log("AUTH_SUCCESS", username, "Login successful")
                return True
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    self.send_message({
                        "type": "auth_error",
                        "content": f"Wrong password (attempt {attempt + 1}/{max_attempts}). Try again:"
                    })
                else:
                    self.send_message({
                        "type": "auth_error",
                        "content": f"Wrong password (attempt {max_attempts}/{max_attempts}). Connection closed."
                    })
                    self.logger.log("AUTH_FAILED", username, f"Too many wrong attempts")
                    return False

        return False

    def _create_new_account(self, username, password_manager):
        """Handle account creation for new user"""
        self.send_message({
            "type": "auth",
            "action": "register",
            "content": "New account. Choose password (min 8 chars, with Upper, lower, digit, special):"
        })

        while True:
            # Get password
            password_data = self.receive_message()
            if not password_data or "password" not in password_data:
                return False

            password = password_data["password"]

            # Validate password
            is_valid, errors = password_manager.validate_password(password)

            if not is_valid:
                error_msg = "\n".join([f"  - {e}" for e in errors])
                entropy, strength, percentage = EntropyCalculator.calculate(password)
                self.send_message({
                    "type": "auth_error",
                    "content": f"Password validation failed:\n{error_msg}\nStrength: {percentage}% ({strength})\n\nTry again:"
                })
                continue

            # Show strength and check if it's acceptable
            entropy, strength, percentage = EntropyCalculator.calculate(password)
            
            if strength == "WEAK":
                self.send_message({
                    "type": "auth_error",
                    "content": f"Password too weak: {percentage}% (WEAK). Must be at least MEDIUM strength (40+ bits). Try again:"
                })
                continue
            
            self.send_message({
                "type": "auth_info",
                "content": f"Password strength: {percentage}% ({strength}). Re-enter to confirm:"
            })

            # Confirm password
            confirm_data = self.receive_message()
            if not confirm_data or "password" not in confirm_data:
                return False

            confirm_password = confirm_data["password"]

            if password != confirm_password:
                self.send_message({
                    "type": "auth_error",
                    "content": "Passwords don't match. Try again:"
                })
                continue

            # Save user (hashed password for authentication)
            password_manager.add_user(username, password)
            
            # Derive and save encryption key for this user
            PasswordManager.save_user_key(username, password)
            
            self.send_message({
                "type": "auth_success",
                "content": f"Account created! Welcome {username}!"
            })
            self.logger.log("AUTH_REGISTER", username, "New account created")
            return True
    
    def register_public_key(self, username, public_key_pem_b64):
        """
        Register user's public key in the server registry (JOUR3_PARTIE1).
        
        Args:
            username (str): Username
            public_key_pem_b64 (str): Base64-encoded PEM public key
        
        Returns:
            bool: True if registration succeeded
        """
        try:
            with self.registry_lock:
                self.public_key_registry[username] = public_key_pem_b64
                self.logger.log("RSA_REGISTER", username, f"Public key registered")
                return True
        except Exception as e:
            self.logger.error(f"Failed to register public key for {username}: {e}")
            return False
    
    def send_public_key_registry(self):
        """
        Send the public key registry to the client (JOUR3_PARTIE1).
        
        Used so clients can retrieve public keys for key exchange.
        """
        try:
            with self.registry_lock:
                # Send registry (dict of {username: public_key_pem_b64})
                self.send_message({
                    "type": "public_key_registry",
                    "registry": dict(self.public_key_registry)
                })
        except Exception as e:
            self.logger.error(f"Failed to send public key registry: {e}")

    def run(self):
        """Main client handler loop"""
        # Initialize password manager
        password_manager = PasswordManager()
        
        # Request username
        self.send_message({"type": "username_request"})
        username_data = self.receive_message()

        if not username_data or "username" not in username_data:
            self.client_socket.close()
            return

        username = username_data["username"].strip()

        # Validate username format
        if len(username) < 3:
            self.send_message({"type": "error", "content": "Username must be at least 3 characters"})
            self.client_socket.close()
            return

        # Check if username already connected simultaneously
        if username in self.all_users:
            self.send_message({"type": "error", "content": "Username already taken"})
            self.client_socket.close()
            return

        # Authenticate user
        if not self._authenticate_user(username, password_manager):
            self.client_socket.close()
            return

        self.username = username
        self.all_users[username] = self.client_socket

        # Join default room
        self.room_manager.join_room("general", username, self.client_socket)
        self.logger.log("CONNECT", username, f"Authenticated connection from {self.client_address}")

        # Send welcome message
        self.send_message({
            "type": "welcome",
            "content": f"Welcome to Crypto Vibeness, {username}!",
            "color": self.get_user_color(username)
        })

        # Notify others
        self.broadcast_to_room({
            "type": "system",
            "content": f"{username} has joined the chat"
        }, exclude_sender=True)

        # Main loop
        while True:
            msg = self.receive_message()
            if msg is None:
                break

            msg_type = msg.get("type", "")

            if msg_type == "command":
                if not self.handle_command(msg):
                    break
            elif msg_type == "public_key":
                # Register public key with server (JOUR3_PARTIE1)
                public_key_b64 = msg.get("public_key_b64")
                if public_key_b64:
                    self.register_public_key(self.username, public_key_b64)
            elif msg_type == "registry_request":
                # Send current public key registry to client (JOUR3_PARTIE1)
                self.send_public_key_registry()
            elif msg_type == "message":
                # Broadcast message to room
                timestamp = datetime.now().strftime("%H:%M:%S")
                color = self.get_user_color(self.username)

                broadcast_msg = {
                    "type": "message",
                    "from": self.username,
                    "room": self.current_room,
                    "content": msg.get("content", ""),
                    "timestamp": timestamp,
                    "color": color
                }
                
                # Add encrypted content if present (JOUR2_PARTIE2)
                if "encrypted_content" in msg:
                    broadcast_msg["encrypted_content"] = msg.get("encrypted_content")
                    broadcast_msg["iv"] = msg.get("iv")
                
                # Verify signature if present (JOUR3_PARTIE2)
                signature_valid = False
                if "signature" in msg and self.username in self.public_key_registry:
                    try:
                        signature = msg.get("signature")
                        plaintext = msg.get("content", "")  # Use plaintext for signature verification
                        
                        # Get sender's public key from registry
                        sender_pub_b64 = self.public_key_registry.get(self.username)
                        if sender_pub_b64:
                            sender_pub_pem = base64.b64decode(sender_pub_b64)
                            sender_pub_key = RSACrypto.pem_to_public_key(sender_pub_pem)
                            
                            # Verify signature
                            signature_valid = RSASignature.verify(sender_pub_key, plaintext, signature)
                            broadcast_msg["signature_valid"] = signature_valid
                            
                            if signature_valid:
                                self.logger.log("SIGNATURE", self.username, "Message signature verified ✓")
                            else:
                                self.logger.log("SIGNATURE", self.username, "Message signature INVALID ✗")
                    except Exception as e:
                        self.logger.error(f"Failed to verify signature: {e}")

                self.logger.log("MESSAGE", self.username, f"{self.current_room}: {msg.get('content', '')}")
                self.broadcast_to_room(broadcast_msg)
            
            elif msg_type == "session_key_offer":
                # Forward session key offer to recipient (JOUR3_PARTIE1)
                to_user = msg.get("to", "")
                if to_user and to_user in self.all_users:
                    try:
                        forward_msg = {
                            "type": "session_key_offer",
                            "from": self.username,
                            "to": to_user,
                            "encrypted_session_key_b64": msg.get("encrypted_session_key_b64")
                        }
                        target_socket = self.all_users[to_user]
                        target_socket.sendall((json.dumps(forward_msg) + "\n").encode('utf-8'))
                        self.logger.log("SESSION_KEY", self.username, f"Session key offer sent to {to_user}")
                    except Exception as e:
                        self.logger.error(f"Failed to forward session key offer: {e}")

        # Cleanup
        self.room_manager.leave_room(self.current_room, self.username)
        del self.all_users[self.username]
        self.client_socket.close()
        self.logger.log("DISCONNECT", self.username, "Disconnected")

        # Notify others
        room = self.room_manager.get_room(self.current_room)
        if room:
            clients = room.get_clients()
            for client_socket in clients.values():
                try:
                    msg = json.dumps({
                        "type": "system",
                        "content": f"{self.username} has left the chat"
                    }) + "\n"
                    client_socket.sendall(msg.encode('utf-8'))
                except:
                    pass


class ChatServer:
    """Main chat server"""

    def __init__(self, config_file="src/config/config.json"):
        # Load config
        with open(config_file, 'r') as f:
            self.config = json.load(f)

        self.port = self.config["server"]["default_port"]
        self.host = self.config["server"]["host"]
        self.room_manager = RoomManager()
        self.all_users = {}
        self.logger = CryptoLogger()
        self.running = False
        
        # Public key registry (JOUR3_PARTIE1)
        # Format: {username: public_key_pem_b64}
        self.public_key_registry = {}
        self.registry_lock = threading.Lock()

    def start(self):
        """Start the server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(self.config["server"]["max_clients"])
            self.logger.info(f"Server listening on {self.host}:{self.port}")
            self.running = True

            while self.running:
                try:
                    client_socket, client_address = server_socket.accept()
                    self.logger.info(f"New connection from {client_address}")

                    # Create handler thread
                    handler = ClientHandler(
                        client_socket,
                        client_address,
                        self.room_manager,
                        self.all_users,
                        self.logger,
                        self.config,
                        self.public_key_registry,
                        self.registry_lock
                    )
                    handler.start()
                except KeyboardInterrupt:
                    self.logger.info("Server shutting down...")
                    break
                except Exception as e:
                    self.logger.error(f"Error accepting connection: {e}")

        except Exception as e:
            self.logger.error(f"Server error: {e}")
        finally:
            server_socket.close()
            self.logger.info("Server stopped")


if __name__ == "__main__":
    server = ChatServer()
    server.start()
