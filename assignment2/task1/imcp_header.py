# @author: Malthe Tøttrup

import struct

"""
The ICMP header is defined as follows: https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Type(8)   |     Code(0)   |          Checksum             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Identifier          |        Sequence Number        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                             Payload                           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""

def imcp_header(message):
    # Create the ICMP header with a payload
    type = 47  # ICMP echo request
    code = 0
    checksum = 0  # Set to 0 for now, will be calculated later
    identifier = 1234
    seqnum = 1
    payload = message

    icmp_header = struct.pack("!BBHHH", type, code, checksum, identifier, seqnum) + payload

    # Calculate the ICMP checksum
    checksum = 0
    
    # in case the length is odd we need to add padding
    if len(icmp_header) % 2 == 1: 
        icmp_header += b'\x00'

    for i in range(0, len(icmp_header), 2):
        checksum += (icmp_header[i] << 8) + icmp_header[i+1]

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = ~checksum & 0xffff

    # Pack the checksum back into the header
    icmp_header = struct.pack("!BBHHH", type, code, checksum, identifier, seqnum) + payload

    return icmp_header
