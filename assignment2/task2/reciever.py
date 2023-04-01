import socket

# set up a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set up the address and port to listen on
host = '127.0.0.1' # replace with your IP address
port = 8000

# bind the socket to the address and port
s.bind((host, port))

# listen for incoming connections
s.listen(1)

# accept the incoming connection
conn, addr = s.accept()
print('Connection from', addr)

# receive the data from the sender
data = b''
while True:
    packet = conn.recv(1024)
    if not packet:
        break
    data += packet

# write the data to a file
with open('received_meme.png', 'wb') as f:
    f.write(data)

# close the connection and the socket
conn.close()
s.close()