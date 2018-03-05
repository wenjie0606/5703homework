import socket
import nltk
import json
import sys

# create an INET socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the host and a port
port=sys.argv[1]
server_socket.bind(("localhost", int(port)))
print("Listening for incoming connections on port %s" % port)

# Listen for incoming connections from clients
server_socket.listen(1)

# A indefinite loop
while True:
    # accept connections from outside
    (client_socket, address) = server_socket.accept()
    print("Client %s connected." %(address[0]))

    data=[]

    # Read data from client and send it back
    # part = client_socket.recv(2048)

    #check the end of the txt
    while True:
        part = client_socket.recv(2048)
        if b'[END]' not in part:
            data.append(part)
        else:
            data.append(part[:part.find(b'[END]')])
            break

    # convert list to string
    data0=b"".join(data)

    print(data0.decode("utf-8"))

    tokens = nltk.word_tokenize(data0.decode("utf-8"))
    tagged = nltk.pos_tag(tokens)

    client_socket.sendall(json.dumps(tagged).encode())

    # Close the socket
    print("Client disconnected.")
    client_socket.close()
