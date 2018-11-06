from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv


# assign line arguments
my_port = int(argv[1])
parent_ip = argv[2]
parent_port = int(argv[3])
file_name = argv[4]

source_ip = "127.0.0.1"  # local ip for the server to bind to

# open and read the ip mapping from the given file
ip_file = open(file_name, 'r')
lines = ip_file.read().split('\n')
ip_file.close()

# open the file to append new addresses if needed
ip_file = open(file_name, 'a')

# create and bint the socket
soc_this = socket(AF_INET, SOCK_DGRAM)
soc_this.bind((source_ip, my_port))

# create socket for the parent server
soc_parent = socket(AF_INET, SOCK_DGRAM)

# create the address-ip mapping dictionary
ips = {}
for line in lines:
    comma = line.find(',')
    ips[line[:comma]] = line[comma+1:]


def add_ip(addr, ip):
    """
    the function adds the new mapping to the dictionary
    and learns it by appending it to the file
    :param addr: new address to add and learn
    :param ip: the ip mapping of the given address
    """
    ips[addr] = ip  # add to dictionary
    ip_file.write(addr + ',' + ip + '\n')  # append to file


def ask_parent(addr):
    """
    the function asks the parent server an ip mapping
    for an unknown address and learns it
    :param addr: unknown address to forward to the parent server
    :return: the ip mapping for the given server, or "NO IP" if it is unknown
    """
    # if the server has no parent then the ip is unknown
    if parent_ip == "-1" or parent_port == -1:
        return "NO IP"

    # else ask the parent for the ip and receive an answer
    soc_parent.sendto(addr, (parent_ip, parent_port))
    _data, _sender_info = soc_parent.recvfrom(2048)

    # if the ip exists in parent then learn it
    if not _data == "NO IP":
        add_ip(addr, _data)

    # return the ip
    return _data


data = ""
while True:
    # receive address question from client
    data, sender_info = soc_this.recvfrom(2048)

    # if the address is known then give the answer
    if ips.__contains__(data):
        ans = ips[data]

    # else ask the parent server
    else:
        ans = ask_parent(data)

    # send the answer to the client
    soc_this.sendto(ans, sender_info)
