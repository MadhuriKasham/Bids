import socket
import threading
import time
HEAD = 50
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECTED"
# SERVER = '192.168.56.1'
SERVER = socket.gethostbyname(socket.gethostname())
# print(SERVER)
# print(socket.gethostbyname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    connected = True
    while connected:
        print(f"new connection {addr} connected")
        msg_length = conn.recv(HEAD).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            if msg == DISCONNECT_MESSAGE:
                connected = False

                
    conn.close()

    

def start():
    server.listen()
    print(f"server on {SERVER}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target= handle_client, args= (conn,addr))
        thread.start()
        print(f"active therads {threading.activeCount() -1}")


print("server started")

start()

