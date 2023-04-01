# make a server that listens on port 8080

import socket
import struct
from Crypto.Cipher import AES

def server():
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.SOCK_STREAM)

    key = b'\xb00\xecL\xdf\x1eK.\xcf|l\x1d\xc2aC\xb1' # shared key

    # get local machine name
    host = socket.gethostname()

    # bind the socket to the ICMP protocol
    server_socket.bind((host, socket.IPPROTO_ICMP))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data, addr = server_socket.recvfrom(1024)

        icmp_header = data[20:28]
        type, code, checksum, identifier, seqnum = struct.unpack("!BBHHH", icmp_header)
        payload = data[28:]
        # decrypt the message
        nonce = payload[:16]
        tag = payload[16:32]
        ciphertext = payload[32:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        message = cipher.decrypt_and_verify(ciphertext, tag)

        if not data:
            # if data is not received break
            break
        print("Message from client: " + message.decode('utf-8'))

    server_socket.close()

if __name__ == '__main__':
    server()