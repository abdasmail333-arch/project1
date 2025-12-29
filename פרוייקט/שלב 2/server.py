import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}
lock = threading.Lock()

def broadcast(sender, message):
    with lock:
        for name, conn in list(clients.items()):
            if name != sender:
                try:
                    conn.sendall(f"{sender}: {message}\n".encode("utf-8"))
                except:
                    pass

def handle_client(conn, addr):
    try:
        conn.sendall("הכנס שם:\n".encode("utf-8"))
        name = conn.recv(1024).decode("utf-8").strip()

        if not name:
            conn.close()
            return

        with lock:
            if name in clients:
                conn.sendall("השם תפוס\n".encode("utf-8"))
                conn.close()
                return
            clients[name] = conn

        conn.sendall("מחובר\n".encode("utf-8"))
        broadcast("SERVER", f"{name} הצטרף")

        while True:
            data = conn.recv(4096)
            if not data:
                break

            msg = data.decode("utf-8").strip()
            if msg.lower() == "/quit":
                break

            broadcast(name, msg)

    except:
        pass
    finally:
        with lock:
            remove_name = None
            for n, c in clients.items():
                if c == conn:
                    remove_name = n
                    break
            if remove_name:
                del clients[remove_name]
                broadcast("SERVER", f"{remove_name} יצא")

        try:
            conn.close()
        except:
            pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("Server running")

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    main()
