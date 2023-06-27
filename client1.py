import socket
s = socket.socket() # socket object
port = 6789 # choose aport
s.connect(('100.0.0.1', port))
print(s.recv(100))
s.close()
