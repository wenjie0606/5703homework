import socket
import json
import sys

# create an INET TCP socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server (change localhost to an IP address if necessary)
try:
    soc.connect((sys.argv[1], int(sys.argv[2])))
    print("Connected to server.")
except Exception as err:
    print("Cannot connect to server at %s:%i" % ("localhost" ,55703))

#'/Users/wenjiexu/Documents/file.txt'
with open(sys.argv[3], 'rb') as f:
    msg = f.read()
    msg = msg+b'[END]'

# Send a message to the server
soc.send(msg)

# Receive data from the server
datasum=bytearray()

while True:
    data = soc.recv(2048)

    if data:
        datasum.extend(data)
    else:
        break


datastr= datasum.decode("utf-8")
dedata = json.loads(datastr)

dedata0 = [dedata[i][0] for i in range(0,len(dedata))]
dedata1 = [dedata[i][1] for i in range(0,len(dedata))]

print(";".join(dedata0))
print(";".join(dedata1))
# Always close the socket after use'''
soc.close()

