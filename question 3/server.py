from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv


my_port = int(argv[1])
parent_ip = argv[2]
parent_port = int(argv[3])
file_name = argv[4]

source_ip = "127.0.0.1"

ip_file = open(file_name, 'r')
lines = ip_file.read().split('\n')
ip_file.close()
ip_file = open(file_name, 'a')

soc_this = socket(AF_INET, SOCK_DGRAM)
soc_this.bind((source_ip, my_port))

soc_parent = socket(AF_INET, SOCK_DGRAM)

ips = {}
for line in lines:
    comma = line.find(',')
    ips[line[:comma]] = line[comma+1:]


def add_ip(addr, ip):
    ips[addr] = ip
    ip_file.write(addr + ',' + ip + '\n')


def ask_parent(addr):
    if parent_ip == "-1" or parent_port == -1:
        return "NO IP"

    soc_parent.sendto(addr, (parent_ip, parent_port))
    _data, _sender_info = soc_parent.recvfrom(2048)

    if not _data == "NO IP":
        add_ip(addr, _data)
    return _data


data = ""
while True:
    data, sender_info = soc_this.recvfrom(2048)
    if ips.__contains__(data):
        ans = ips[data]
    else:
        ans = ask_parent(data)
    soc_this.sendto(ans, sender_info)
