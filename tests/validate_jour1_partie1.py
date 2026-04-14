"""
Validation script for JOUR1 PARTIE1 - YOLO Chat
"""
import socket
import json
import time
import threading
import os


def check_criterion(name, result):
    """Print validation result"""
    symbol = "✅" if result else "❌"
    print(f"{symbol} {name}")
    return result


def test_all_criteria():
    """Test all validation criteria"""
    print("\n" + "=" * 70)
    print("JOUR1 PARTIE1 - YOLO CHAT VALIDATION")
    print("=" * 70 + "\n")
    
    results = {}
    
    # 1. Server listening
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect(("localhost", 5555))
        sock.close()
        results["server_listening"] = True
    except:
        results["server_listening"] = False
    check_criterion("1. Server listening on port 5555", results["server_listening"])
    
    # 2. Client can connect and choose username
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 5555))
        
        # Receive username request
        data = json.loads(sock.recv(4096).decode('utf-8'))
        
        # Send username
        sock.sendall((json.dumps({"username": "test_user_1"}) + "\n").encode('utf-8'))
        
        # Receive welcome
        data = json.loads(sock.recv(4096).decode('utf-8'))
        sock.close()
        results["client_connect"] = data.get("type") == "welcome"
    except:
        results["client_connect"] = False
    check_criterion("2. Client can connect and receive welcome", results["client_connect"])
    
    # 3. Username uniqueness
    try:
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(("localhost", 5555))
        json.loads(sock1.recv(4096).decode('utf-8'))  # username request
        sock1.sendall((json.dumps({"username": "unique_test"}) + "\n").encode('utf-8'))
        json.loads(sock1.recv(4096).decode('utf-8'))  # welcome
        
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(("localhost", 5555))
        json.loads(sock2.recv(4096).decode('utf-8'))  # username request
        sock2.sendall((json.dumps({"username": "unique_test"}) + "\n").encode('utf-8'))
        
        # Should get error
        data = json.loads(sock2.recv(4096).decode('utf-8'))
        results["username_unique"] = data.get("type") == "error"
        
        sock1.close()
        sock2.close()
    except:
        results["username_unique"] = False
    check_criterion("3. Usernames are unique", results["username_unique"])
    
    # 4. Default room exists
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 5555))
        json.loads(sock.recv(4096).decode('utf-8'))
        sock.sendall((json.dumps({"username": "test_rooms"}) + "\n").encode('utf-8'))
        json.loads(sock.recv(4096).decode('utf-8'))
        
        sock.sendall((json.dumps({"type": "command", "command": "rooms", "args": []}) + "\n").encode('utf-8'))
        data = json.loads(sock.recv(4096).decode('utf-8'))
        
        results["default_room"] = "general" in str(data.get("content", []))
        sock.close()
    except:
        results["default_room"] = False
    check_criterion("4. Default 'general' room exists", results["default_room"])
    
    # 5. Messages broadcast to room
    try:
        # User 1 sends message
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(("localhost", 5555))
        json.loads(sock1.recv(4096).decode('utf-8'))
        sock1.sendall((json.dumps({"username": "sender"}) + "\n").encode('utf-8'))
        json.loads(sock1.recv(4096).decode('utf-8'))
        
        # User 2 joins
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(("localhost", 5555))
        json.loads(sock2.recv(4096).decode('utf-8'))
        sock2.sendall((json.dumps({"username": "receiver"}) + "\n").encode('utf-8'))
        json.loads(sock2.recv(4096).decode('utf-8'))
        
        # User 2 should get join notification
        sock2.settimeout(1)
        data = json.loads(sock2.recv(4096).decode('utf-8'))
        
        # User 1 sends message
        sock1.sendall((json.dumps({"type": "message", "content": "Hello world"}) + "\n").encode('utf-8'))
        
        # User 1 gets echo
        sock1.settimeout(1)
        data1 = json.loads(sock1.recv(4096).decode('utf-8'))
        
        # User 2 gets message
        sock2.settimeout(1)
        data2 = json.loads(sock2.recv(4096).decode('utf-8'))
        
        results["message_broadcast"] = (
            data1.get("type") == "message" and 
            data2.get("type") == "message" and
            "Hello world" in str(data2.get("content", ""))
        )
        
        sock1.close()
        sock2.close()
    except Exception as e:
        results["message_broadcast"] = False
        print(f"   Error: {e}")
    check_criterion("5. Messages broadcast correctly", results["message_broadcast"])
    
    # 6. Logs file exists
    log_dir = "data/logs"
    results["logs_exist"] = os.path.exists(log_dir) and len(os.listdir(log_dir)) > 0
    check_criterion("6. Logs file created", results["logs_exist"])
    
    # 7. Commands work
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 5555))
        json.loads(sock.recv(4096).decode('utf-8'))
        sock.sendall((json.dumps({"username": "cmd_test"}) + "\n").encode('utf-8'))
        json.loads(sock.recv(4096).decode('utf-8'))
        
        # Test /help
        sock.sendall((json.dumps({"type": "command", "command": "help", "args": []}) + "\n").encode('utf-8'))
        sock.settimeout(1)
        data = json.loads(sock.recv(4096).decode('utf-8'))
        results["help_command"] = data.get("type") == "help"
        
        sock.close()
    except:
        results["help_command"] = False
    check_criterion("7. /help command works", results["help_command"])
    
    # 8. Room creation
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 5555))
        json.loads(sock.recv(4096).decode('utf-8'))
        sock.sendall((json.dumps({"username": "room_test"}) + "\n").encode('utf-8'))
        json.loads(sock.recv(4096).decode('utf-8'))
        
        # Create room
        sock.sendall((json.dumps({"type": "command", "command": "create", "args": ["test_room"]}) + "\n").encode('utf-8'))
        sock.settimeout(1)
        data = json.loads(sock.recv(4096).decode('utf-8'))
        results["room_create"] = data.get("type") == "system" and "created" in data.get("content", "").lower()
        
        sock.close()
    except:
        results["room_create"] = False
    check_criterion("8. Room creation works", results["room_create"])
    
    # 9. /users command
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 5555))
        json.loads(sock.recv(4096).decode('utf-8'))
        sock.sendall((json.dumps({"username": "users_test"}) + "\n").encode('utf-8'))
        json.loads(sock.recv(4096).decode('utf-8'))
        
        sock.sendall((json.dumps({"type": "command", "command": "users", "args": []}) + "\n").encode('utf-8'))
        sock.settimeout(1)
        data = json.loads(sock.recv(4096).decode('utf-8'))
        results["users_command"] = data.get("type") == "users" and isinstance(data.get("content"), list)
        
        sock.close()
    except:
        results["users_command"] = False
    check_criterion("9. /users command works", results["users_command"])
    
    # Summary
    print("\n" + "=" * 70)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"RESULTS: {passed}/{total} criteria passed")
    
    if passed == total:
        print("🎉 JOUR1_PARTIE1 ✅ VALIDATED")
    else:
        print("⚠️  Some criteria failed")
    
    print("=" * 70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    test_all_criteria()
