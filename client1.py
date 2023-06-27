import socket
s = socket.socket()
port = 6789
s.connect(('100.0.0.1', port))
print(s.recv(100))
s.close()
