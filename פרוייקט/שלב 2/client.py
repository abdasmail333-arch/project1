import socket
import threading
import sys

SERVER_IP = "127.0.0.1"
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            print(data.decode("utf-8"), end="")
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    t = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    t.start()

    while True:
        msg = sys.stdin.readline()
        if not msg:
            break
        client.sendall(msg.encode("utf-8"))
        if msg.strip().lower() == "/quit":
            break

    try:
        client.close()
    except:
        pass

if __name__ == "__main__":
    main()
