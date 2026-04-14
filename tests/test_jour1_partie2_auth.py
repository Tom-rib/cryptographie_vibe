"""
Test script for JOUR1_PARTIE2 - Authentication
"""
import socket
import json
import time
import threading


def test_client(username, password, confirm_password=None):
    """Test client authentication"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5555))
    
    print(f"\n[{username}] Connected")
    
    # Receive username request
    msg = json.loads(sock.recv(4096).decode('utf-8'))
    print(f"[{username}] <- {msg['type']}")
    
    # Send username
    sock.sendall((json.dumps({"username": username}) + "\n").encode('utf-8'))
    print(f"[{username}] -> username: {username}")
    
    # Receive auth prompt
    data = sock.recv(4096).decode('utf-8')
    for line in data.strip().split('\n'):
        if line:
            msg = json.loads(line)
            print(f"[{username}] <- {msg['type']}: {msg.get('content', '')[:60]}")
            
            if msg['type'] in ['auth', 'auth_error', 'auth_info']:
                # Send password
                sock.sendall((json.dumps({"password": password}) + "\n").encode('utf-8'))
                print(f"[{username}] -> password: {'*' * len(password)}")
                
                # If confirmation needed
                if confirm_password is not None and msg['type'] == 'auth_info':
                    time.sleep(0.1)
                    data2 = sock.recv(4096).decode('utf-8')
                    for line2 in data2.strip().split('\n'):
                        if line2:
                            msg2 = json.loads(line2)
                            print(f"[{username}] <- {msg2['type']}: {msg2.get('content', '')[:60]}")
    
    # Receive more messages
    sock.settimeout(1.0)
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            for line in data.decode('utf-8').strip().split('\n'):
                if line:
                    msg = json.loads(line)
                    if msg['type'] == 'auth_success':
                        print(f"[{username}] ✅ {msg.get('content')}")
                        break
                    elif msg['type'] == 'auth_error':
                        print(f"[{username}] ❌ {msg.get('content', '')[:60]}")
                    elif msg['type'] == 'welcome':
                        print(f"[{username}] Welcome message received")
                        break
    except socket.timeout:
        pass
    
    sock.close()
    print(f"[{username}] Disconnected\n")


def run_tests():
    """Run authentication tests"""
    print("=" * 70)
    print("JOUR1_PARTIE2 - AUTHENTICATION TEST")
    print("=" * 70)
    
    # Test 1: New user with strong password
    print("\n[TEST 1] New user - strong password")
    test_client("alice", "SecurePass123!")
    
    time.sleep(1)
    
    # Test 2: New user with weak password
    print("[TEST 2] New user - weak password")
    test_client("bob", "weak")
    
    time.sleep(1)
    
    # Test 3: Existing user - correct password
    print("[TEST 3] Existing user - correct password")
    test_client("alice", "SecurePass123!")
    
    print("\n" + "=" * 70)
    print("TESTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
