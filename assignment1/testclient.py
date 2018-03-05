import socket


# create an INET TCP socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server (change localhost to an IP address if necessary)

soc.connect(("localhost", 50001))




soc.send(b"hello,server")

datasum=bytearray()

while True:
    data = soc.recv(2048)

    print(data)
    if data!=b'':
        datasum.extend(data)
        print(datasum)

    else:
        break

print("connection close")

# Always close the socket after use
soc.close()

