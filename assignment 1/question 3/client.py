from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv


# assign line arguments
server_ip = argv[1]
server_port = int(argv[2])

# create the socket
s = socket(AF_INET, SOCK_DGRAM)

addr = raw_input()
# while not quit
while not addr == 'quit':
    s.sendto(addr, (server_ip, server_port))  # send the address to the server
    data, sender_info = s.recvfrom(2048)  # receive the answer from the server

    print data  # print the ip

    addr = raw_input()

# close the socket
s.close()
