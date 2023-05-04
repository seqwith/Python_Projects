import argparse
import os
import sys
from telnetlib import IP
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from ipaddress import ip_address

def process_pcap(file_name):
    print('Opening {}...'.format(file_name))

    count = 0
    interesting_packets = 0
    # Place holder for the IP addresses
    client_ip = ''
    server_ip = ''
    # Place holder for the ports
    client_port = ''
    server_port = ''


    for (pkt_data, *pkt_metadata,) in RawPcapReader(file_name):
        count += 1
        ether_pkt = Ether(pkt_data)
        if 'type' not in ether_pkt.fields:
            # LLC frames will have 'len' instead of 'type'
            # we can ingnore these.
            continue
        if ether_pkt.type != 0x0800:
            # we are going to disregard non-IPv4 packets (for now)
            continue

        ip_pkt = ether_pkt[IP]

        if ip_pkt.proto != 6:
            # Ignore non-TCP packet
            continue

        if (ip_pkt.src != server_ip) and (ip_pkt.src != client_ip):
            #Unintersting source IP
            continue

        if (ip_pkt.dst != server_ip) and (ip_pkt != client_ip):
            # Uninteresting destination IP
            continue

        tcp_pkt = ip_pkt[TCP]

        if (tcp_pkt.sport != int(server_port)) and \
            (tcp_pkt.sport != int(client_port)):
            # Unintersting source TCP port
            continue

        if (tcp_pkt.dport != int(server_port)) and \
            (tcp_pkt.dport != int(client_port)):
            # Uninteresting destination TCP port
            continue

        interesting_packets += 1

    #---

    print('{} contains {} packets ({} interesting)'.format(file_name, count, interesting_packets))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCAP reader')
    parser.add_argument('--pcap', metavar='<pcap file name>', help='pcap file to parse', required=True)
    parser.add_argument('-c', metavar='<IP Address>', type=ip_address, action='store', dest='client_ip', help='Client IP address', required=False)
    parser.add_argument('-cp', type=int, metavar='<Port>', action='store', dest='client_port', help='Client port', required=False)
    parser.add_argument('-s', type=ip_address, metavar='<IP Address>', action='store', dest='server_ip', help='Server IP address', required=False)
    parser.add_argument('-sp', type=int, metavar='<Port>', action='store', dest='server_port', help='Server Port', required=False)

    args = parser.parse_args()

    file_name = args.pcap
    if not os.path.isfile(file_name):
        print('"{}" does not exist'.format(file_name), file=sys.stderr)
        sys.exit(-1)

    process_pcap(file_name)
    sys.exit(0)