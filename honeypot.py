import socket
import threading
import paramiko
import logging
import datetime
import os
import json

# Setup logging to file
if not os.path.exists("logs"):
    os.makedirs("logs")
LOGFILE = "logs/honeypot.log"
logging.basicConfig(filename=LOGFILE, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Thread-safe JSON logging helpers
attempts_lock = threading.Lock()
commands_lock = threading.Lock()
def log_attempt(event):
    with attempts_lock:
        with open("logs/attempts.json", "a") as f:
            json.dump(event, f)
            f.write("\n")
def log_command(event):
    with commands_lock:
        with open("logs/commands.json", "a") as f:
            json.dump(event, f)
            f.write("\n")

# Load host private key
host_key = paramiko.RSAKey(filename='test_rsa.key')

# Implement SSH ServerInterface
class Server(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.event = threading.Event()
        self.client_ip = client_ip

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        logging.info(f"Auth attempt from {self.client_ip} with username: {username} password: {password}")
        log_attempt({
            "timestamp": str(datetime.datetime.now()),
            "ip": self.client_ip,
            "username": username,
            "password": password,
            "success": False
        })
        if username.startswith('admin') and password == '13@admin123':
            log_attempt({
                "timestamp": str(datetime.datetime.now()),
                "ip": self.client_ip,
                "username": username,
                "password": password,
                "success": True
            })
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
def handle_command(command, channel, client_ip):
    response = ""
    cmd = command.lower()
    if cmd == "ls":
        response = "users.txt"
    elif cmd == "pwd":
        response = "/home/admin"
    else:
        response = f"bash: {cmd}: command not found"

    log_command({"timestamp": str(datetime.datetime.now()), "ip": client_ip, "command": command})
    channel.send(response + "\r\n")
def handle_connection(client_socket, client_addr):
    client_ip = client_addr[0]
    logging.info(f"New connection from {client_ip}")
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(host_key)
        server = Server(client_ip)
        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel is None:
            logging.warning(f"No channel for {client_ip}")
            return
        server.event.wait(10)
        if not server.event.is_set():
            logging.warning(f"Client {client_ip} never asked for shell")
            return
        channel.send("Welcome to Ubuntu 20.04.1 LTS (GNU/Linux x86_64)\r\n\r\n")
        channel.send("$ ")
        while True:
            command = ""
            while not command.endswith("\r"):
                data = channel.recv(1024)
                if not data:
                    break
                command += data.decode('utf-8')
            command = command.strip()
            if not command:
                break
            if command.lower() == "exit":
                channel.send("Bye!\r\n")
                break
            handle_command(command, channel, client_ip)
            channel.send("$ ")
        channel.close()
        transport.close()
        logging.info(f"Connection from {client_ip} closed")
    except Exception as e:
        logging.error(f"Exception handling connection from {client_ip}: {e}")

def start_server(port=2222):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 2222))
    sock.listen(100)
    logging.info(f"SSH Honeypot listening on port {port}...")
    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(client, addr)).start()

if __name__ == "__main__":
    start_server()
