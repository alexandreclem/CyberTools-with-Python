#! /usr/bin/python3
import sys
from datetime import datetime
from scapy.all import *

SYN_ACK = 0x12 
RST = 0x14


def syn_port_scan(port, target_ip):    
    src_port = RandShort()        
    packet = sr1(IP(dst=target_ip)/TCP(sport = src_port, dport=port, flags='S'), timeout=1, verbose=0) # TCP packet with SYN flag.

    if packet != None:
        if packet.haslayer(TCP):
            if packet[TCP].flags == SYN_ACK:
                rst_packet = IP(dst=target_ip)/TCP(sport=src_port, dport=port, flags='R') # Ending the connection (stealth), TCP packet with RST flag
                sr(packet, timeout=1, verbose=0)
                return 'OPN' # Open
            elif packet[TCP].flags == RST:
                return 'CLS' # Closed 
            else:
                return 'FIL' # Filtered
        elif packet.haslayer(ICMP):
            return 'FIL'
        else: 
            return 'UNK'     # Unknown responsed
    else:
        return 'UNS'         # Unanswered


def check_host(host_ip):    
    try:
        ping = sr1(IP(dst=host_ip)/ICMP(), timeout=2, verbose=0)        
    except Exception:
        print("[~] Error, Couldn't Resolve Target.")        
        sys.exit(1)


def main():
    print('\t/-------------- PORT SCAN ATTACK (TCP) --------------/')
    try:        
        target_ip = input('[*] Enter Target IP Address: ')
        try:
            min_port = int(input('[*] Enter Minimum Port Number: '))
            max_port = int(input('[*] Enter Maximum Port Number: '))
        except Exception:
            print('[~] ERROR, Invalid Ports.')        
        
        if int(min_port) >= 0 and int(max_port) >=0 and int(max_port) >= int(min_port):
            pass
        else:
            print('[~] ERROR, Invalid Range of Ports.')               
            sys.exit(1)       

    except KeyboardInterrupt:        
        print('\n[!] Exiting...')
        sys.exit(1)   

    check_host(target_ip)   
    
    ports = range(int(min_port), int(max_port) + 1)     
    print('[!] Scanning started...')  
    for port in ports:        
        status = syn_port_scan(port, target_ip)
        if status == 'OPN':
            print('Port ' + str(port) + ' -> OPEN')    
        elif status == 'CLS':
            print('Port ' + str(port) + ' -> CLOSED')    
        elif status == 'F':
            print('Port ' + str(port) + ' -> FILTERED')    
        elif status == 'UNK':
            print('Port ' + str(port) + ' -> UNKNOWN')    
        else:
            print('Port ' + str(port) + ' -> UNANSWERED')        
    

    print('[!] Scan successfuly done.')  


if __name__ == '__main__':
    main()