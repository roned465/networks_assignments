from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv


server_ip = argv[1]
server_port = int(argv[2])

s = socket(AF_INET, SOCK_DGRAM)

addr = raw_input()
while not addr == 'quit':
    s.sendto(addr, (server_ip, server_port))
    data, sender_info = s.recvfrom(2048)
    print data
    addr = raw_input()
s.close()
