from socket import socket, AF_INET, SOCK_STREAM


source_ip = '0.0.0.0'
source_port = 8080
max_clients_num = 1

# create the socket
s = socket(AF_INET, SOCK_STREAM)
# bind the socket to the port
s.bind((source_ip, source_port))
# listen for clients
s.listen(max_clients_num)

while True:
    # accept a message from a client
    connection, sender_info = s.accept()
    data = connection.recv(2048)

    # pull out the GET request from the data sent
    request = data.split('\r\n')[0]
    request_parts = request.split(' ')

    # if it is not a valid GET request then ignore
    if not (len(request) > 0 and request_parts[0] == "GET"):
        continue

    # pull out the message which is the path to the requested file
    message = request_parts[1].replace('/', '\\')

    # if the message is empty then send the index.html file with state 200 OK
    if message == "\\":
        f = open("files\\index.html", "rb")
        message_to_send = "HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n"
        data_to_send = f.read()
        f.close()

    # if the message is redirect then send state 301 Moved Permanently and redirect to result.html
    elif message == "\\redirect":
        message_to_send = "HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n"
        data_to_send = ""

    # else then a file is requested
    else:
        # try to open the file and send it if succeeded with state 200 OK
        try:
            f = open("files\\" + message[1:], "rb")
            message_to_send = "HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n"
            data_to_send = f.read()
            f.close()

        # if could not open then file does not exist and send state 404 Not Found
        except IOError:
            message_to_send = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"
            data_to_send = ""

    # send the message with the file to the client
    connection.sendall(message_to_send + data_to_send)
