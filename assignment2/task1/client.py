import socket
import argparse
from imcp_header import imcp_header
from Crypto.Cipher import AES
import secrets

def client(dest_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((dest_ip, 0))  # ICMP does not use ports, so we can use 0
    key = b'\xb00\xecL\xdf\x1eK.\xcf|l\x1d\xc2aC\xb1' # shared key

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':

        message = bytes(message, 'utf-8')
        nonce = secrets.token_bytes(16)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(message)
        encrypted_msg = nonce + tag + ciphertext

        imcp_packet = imcp_header(encrypted_msg)

        client_socket.sendto(imcp_packet, (socket.gethostname(), 0))  # send message

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Covert channel client program.')
    parser.add_argument('destination_ip', help='Destination IP address to listen for connections')
    args = parser.parse_args()
    client(dest_ip=args.destination_ip)