import socket

# set up a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set up the address and port of the receiver
host = '127.0.0.1' # replace with the IP address of the receiver
port = 8000

# connect to the receiver
s.connect((host, port))

# open the image file and read the data
with open('meme.png', 'rb') as f:
    data = f.read()

# send the data over the socket
s.sendall(data)

# close the socket
s.close()