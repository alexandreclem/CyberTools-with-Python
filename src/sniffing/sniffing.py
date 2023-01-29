#! /usr/bin/python3

'''
Remember to set the NIC(Network Interface Card) to 
promiscous mode!
'''

import sys
import io
from contextlib import redirect_stdout

from scapy.all import *


def discovering_hosts(net_ip):
    print('[-] Discovering hosts...')    
    eth = Ether(dst='ff:ff:ff:ff:ff:ff') # Broadcast
    arp = ARP(pdst=net_ip) # layer 2 protocol
    packet = eth/arp # creating the packet
    ans, uns = srp(packet, timeout=2, verbose=0) # sending and receiving ans(answered) and uns(unanswered) responses
    
    # Getting the output from answered packets (by default stdout)
    std_out = ''    
    with io.StringIO() as buffer, redirect_stdout(buffer):
        ans.summary(lambda s, r: r.sprintf('%Ether.src% %ARP.psrc%'))   
        std_out = buffer.getvalue()        
   
    print('\n[!] Hosts disponíveis:')
    print('MAC               IP')
    print(f'{std_out}')
   

def sniffing_attack(interface, filter, time_sniffing, results_path):          
    print('[-] Sniffing started...')
    
    # Getting the output from sniffing (by default stdout)
    std_out = ''    
    with io.StringIO() as buffer, redirect_stdout(buffer):
        packets = sniff(iface=interface, filter=filter, timeout=time_sniffing, prn=lambda p: p.summary())
        std_out = buffer.getvalue()     
    
    # Saving the results from sniffing into a txt and pcap files    
    pcap_path = results_path + '/results.pcap'
    results_path = results_path + '/results.txt'
    try:
        results = open('results.txt', 'w')
        results.write(str(std_out))
        results.close()
        wrpcap(pcap_path, packets)     
    except Exception:
        print('[~] ERROR Invalid path.')

    return packets   


def main():
    print('\t/-------------- SNIFFING ATTACK --------------/')
    try:       
        interface = input('[*] Enter Network Interface: ')
        net_ip = input('[*] Enter LAN IP and Mask (Ex:192.168.56.0/24): ')        
        discovering_hosts(net_ip)            
        target_ip = input('[*] Enter Target IP: ')        
        target_port = input('[*] Enter Target Port (Press Enter if ALL): ')
        pcap_path = input('[*] Enter Path to Store the Results (without file name): ')
        try:
            time_sniffing = int(input('[*] Time Sniffing (seconds): '))
        except Exception:
            print('[~] ERROR Invalid time sniffing.')
        if target_port == '':
            filter = f'host {target_ip} and (tcp or udp)'
        else:
            filter = f'host {target_ip} and (tcp or udp) and port {target_port}'        
        
    except KeyboardInterrupt:        
        print('\n[!] Exiting...')
        sys.exit(1)    
    
    packets = sniffing_attack(interface, filter, time_sniffing, pcap_path)       
    print('[!] Sniffing successfuly done.')   

    wshark = input('[*] Do you want to open the results in WIRESHARK ? (yes or no) ')
    if wshark == 'yes':
        wireshark(packets)  


if __name__ == '__main__':
    main()