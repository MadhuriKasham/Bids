import socket
import sys
# try:
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # ip = socket.gethostbyname("www.github.com")
#     # print(ip)
#     print("socket connected successfully")
# except socket.error as err:
#     print(f"socket creation failure{err}")
# port = 80
# try:
#     host_ip = socket.gethostbyname("www.github.com")
# except socket.gaierror:
#     print('error encountered')
#     sys.exit()
# s.connect((host_ip, port))
# print(f"address{host_ip}")

# server methods:

# bind() - ip, port are the parameters,
# listen() - linit the connections
# close() - close the connection
# accept() - accept a client request


import socket
s = socket.socket()
print('Socket created')
port = 6789
s.bind(('', port))
print(f'socket binds with port{port}')
s.listen(3)
print('Socket is listening')
while True:
    c, addr = s.accept()
    print('connection recived from', addr)
    message = ('Thank you for connecting')
    c.send(message.encode())
    c.close()
