"""
Crypto Vibeness Client - IRC-like chat system
Day 1 Part 1: YOLO mode (no authentication, no encryption)
"""
import socket
import json
import threading
import sys
import os
import time


class ChatClient:
    """Client for connecting to Crypto Vibeness chat server"""

    def __init__(self, host="localhost", port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.username = None
        self.running = False
        self.username_requested = False

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
            print(f"\n{msg.get('content')}\n")

        elif msg_type == "message":
            color = msg.get("color", "")
            reset = "\u001b[0m"
            timestamp = msg.get("timestamp", "")
            from_user = msg.get("from", "")
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
                    # Regular message
                    self.send_message({
                        "type": "message",
                        "content": user_input
                    })

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
