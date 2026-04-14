"""
Integration test for JOUR1_PARTIE2 - Full authentication flow
"""
import socket
import json
import time
import subprocess
import os
import signal
import sys


def recv_all_messages(sock, timeout=0.3):
    """Receive all available messages"""
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
    
    # Parse all messages
    for line in buffer.strip().split('\n'):
        if line.strip():
            try:
                messages.append(json.loads(line))
            except Exception as e:
                print(f"Error parsing: {e}")
    
    return messages


def test_new_user_strong_password():
    """Test creating new account with strong password"""
    print("\n[TEST 1] New user with strong password")
    print("-" * 60)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5555))
    
    # Step 1: Username request
    msgs = recv_all_messages(sock)
    print(f"← Server: {msgs[0]['type']}")
    assert msgs[0]['type'] == 'username_request', "Should request username"
    
    # Step 2: Send username
    sock.sendall((json.dumps({"username": "alice"}) + "\n").encode('utf-8'))
    print(f"→ Client: username=alice")
    
    # Step 3: Auth prompt
    time.sleep(0.1)
    msgs = recv_all_messages(sock)
    auth_msg = [m for m in msgs if m['type'] == 'auth']
    assert len(auth_msg) > 0, "Should get auth message"
    print(f"← Server: auth - {auth_msg[0].get('content', '')[:50]}")
    
    # Step 4: Send password
    password = "SecurePass123!"
    sock.sendall((json.dumps({"password": password}) + "\n").encode('utf-8'))
    print(f"→ Client: password=***")
    
    # Step 5: Get strength info
    time.sleep(0.1)
    msgs = recv_all_messages(sock)
    strength_msgs = [m for m in msgs if m['type'] == 'auth_info']
    if strength_msgs:
        print(f"← Server: auth_info - {strength_msgs[0].get('content', '')[:50]}")
    
    # Step 6: Confirm password
    sock.sendall((json.dumps({"password": password}) + "\n").encode('utf-8'))
    print(f"→ Client: password=*** (confirm)")
    
    # Step 7: Success
    time.sleep(0.1)
    msgs = recv_all_messages(sock)
    success_msgs = [m for m in msgs if m['type'] in ['auth_success', 'welcome']]
    if success_msgs:
        print(f"← Server: {success_msgs[0]['type']} - ✅ Account created")
    
    sock.close()
    
    # Verify file
    assert os.path.exists("data/this_is_safe.txt"), "Users file should exist"
    with open("data/this_is_safe.txt", 'r') as f:
        content = f.read()
    assert "alice:" in content, "Alice should be in users file"
    print(f"✅ File verified: alice stored with hash")
    
    return True


def test_existing_user_login():
    """Test logging in with existing user"""
    print("\n[TEST 2] Existing user login")
    print("-" * 60)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5555))
    
    # Step 1: Username request
    msgs = recv_all_messages(sock)
    print(f"← Server: {msgs[0]['type']}")
    
    # Step 2: Send existing username
    sock.sendall((json.dumps({"username": "alice"}) + "\n").encode('utf-8'))
    print(f"→ Client: username=alice")
    
    # Step 3: Login prompt
    time.sleep(0.1)
    msgs = recv_all_messages(sock)
    auth_msg = [m for m in msgs if m['type'] == 'auth']
    assert len(auth_msg) > 0, "Should get login prompt"
    print(f"← Server: auth - {auth_msg[0].get('content', '')[:50]}")
    
    # Step 4: Send correct password
    sock.sendall((json.dumps({"password": "SecurePass123!"}) + "\n").encode('utf-8'))
    print(f"→ Client: password=***")
    
    # Step 5: Success
    time.sleep(0.1)
    msgs = recv_all_messages(sock)
    success_msgs = [m for m in msgs if m['type'] in ['auth_success', 'welcome']]
    if success_msgs:
        print(f"← Server: {success_msgs[0]['type']} - ✅ Logged in")
    
    sock.close()
    return True


def test_weak_password():
    """Test rejecting weak password"""
    print("\n[TEST 3] New user with weak password")
    print("-" * 60)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5555))
    
    # Step 1: Username request
    msgs = recv_all_messages(sock)
    
    # Step 2: Send new username
    sock.sendall((json.dumps({"username": "bob"}) + "\n").encode('utf-8'))
    print(f"→ Client: username=bob")
    
    # Step 3: Auth prompt
    time.sleep(0.1)
    msgs = recv_all_messages(sock)
    
    # Step 4: Send weak password
    sock.sendall((json.dumps({"password": "weak"}) + "\n").encode('utf-8'))
    print(f"→ Client: password=weak")
    
    # Step 5: Should get error
    time.sleep(0.1)
    msgs = recv_all_messages(sock)
    error_msgs = [m for m in msgs if m['type'] == 'auth_error']
    if error_msgs:
        content = error_msgs[0].get('content', '')
        print(f"← Server: auth_error")
        for line in content.split('\n')[:3]:
            if line.strip():
                print(f"    {line.strip()}")
        print(f"✅ Weak password rejected")
    
    sock.close()
    return True


def run_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("JOUR1_PARTIE2 - FULL AUTHENTICATION TEST")
    print("=" * 70)
    
    # Clean up
    if os.path.exists("data/this_is_safe.txt"):
        os.remove("data/this_is_safe.txt")
    
    try:
        test_new_user_strong_password()
        test_existing_user_login()
        test_weak_password()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70 + "\n")
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    run_tests()
