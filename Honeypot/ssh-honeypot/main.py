import socket, sys, threading
import paramiko

host_key = paramiko.RSAKey.generate(2048)

class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        print(f"[!] Login attempt: {username}:{password}")
        return paramiko.AUTH_FAILED  # Never actually allow login

    def get_allowed_auths(self, username):
        return "password"

def handle_client(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(host_key)
    server = SSHServer()
    try:
        transport.start_server(server=server)
    except Exception as e:
        print(f"[-] SSH negotiation failed: {e}")

    transport.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 22))  # WARNING: Needs root
    sock.listen(100)
    print("[*] Fake SSH honeypot listening on port 22...")
    while True:
        client, addr = sock.accept()
        print(f"[+] Connection from {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    main()
