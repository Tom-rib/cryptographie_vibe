"""
Automated test script for Crypto Vibeness chat system
"""
import socket
import json
import time
import threading


def test_client(username, messages, delay=0.5):
    """Simulate a client connection"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5555))
    
    print(f"\n[{username}] Connected")
    
    # Receive username request
    data = sock.recv(4096)
    msg = json.loads(data.decode('utf-8'))
    print(f"[{username}] Server: {msg.get('type')}")
    
    # Send username
    sock.sendall((json.dumps({"username": username}) + "\n").encode('utf-8'))
    
    # Receive welcome
    data = sock.recv(4096)
    msg = json.loads(data.decode('utf-8'))
    print(f"[{username}] Server: {msg.get('content')[:50]}...")
    
    # Send messages
    for msg_text in messages:
        time.sleep(delay)
        
        if msg_text.startswith("/"):
            # Command
            parts = msg_text.split()
            cmd = parts[0][1:]
            args = parts[1:]
            sock.sendall((json.dumps({"type": "command", "command": cmd, "args": args}) + "\n").encode('utf-8'))
            print(f"[{username}] -> Command: {msg_text}")
        else:
            # Message
            sock.sendall((json.dumps({"type": "message", "content": msg_text}) + "\n").encode('utf-8'))
            print(f"[{username}] -> Message: {msg_text}")
        
        # Receive response
        try:
            sock.settimeout(1)
            data = sock.recv(4096)
            while data:
                lines = data.decode('utf-8').split('\n')
                for line in lines:
                    if line:
                        msg = json.loads(line)
                        print(f"[{username}] <- {msg.get('type')}: {str(msg.get('content', msg.get('from', '')))[:50]}")
                data = sock.recv(4096)
        except socket.timeout:
            pass
        except:
            break
    
    sock.close()
    print(f"[{username}] Disconnected\n")


def run_tests():
    """Run multi-client tests"""
    print("=" * 60)
    print("CRYPTO VIBENESS - YOLO MODE TEST")
    print("=" * 60)
    
    # Test 1: Single client
    print("\n[TEST 1] Single client with commands")
    test_client("alice", [
        "/help",
        "/rooms",
        "Hello from alice!",
        "/users",
        "/quit"
    ])
    
    time.sleep(1)
    
    # Test 2: Multiple clients
    print("[TEST 2] Multiple clients communicating")
    
    t1 = threading.Thread(target=test_client, args=("bob", [
        "/users",
        "Hi everyone!",
        "How is it going?",
    ]))
    
    t2 = threading.Thread(target=test_client, args=("charlie", [
        "/users",
        "/rooms",
        "Hello bob!",
    ]))
    
    t1.start()
    time.sleep(0.5)
    t2.start()
    
    t1.join()
    t2.join()
    
    print("\n[TEST 2] Complete")
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
