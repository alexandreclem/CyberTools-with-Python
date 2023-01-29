#! /usr/bin/python3

import threading
from scapy.all import *
from tkinter import *

# Global Variables
SYN_ACK = 0x12 
RST = 0x14
root = Tk()


def check_host(host_ip, results_text):    
    try:
        ping = sr1(IP(dst=host_ip)/ICMP(), timeout=2, verbose=0)          
    except Exception:    
        results_text['state'] = 'normal'
        results_text.insert(END, "[~] Error, Couldn't Resolve Target.\n")
        results_text['state'] = 'disabled' 
        return False         


def syn_port_scan(port, target_ip):    
    src_port = RandShort()        
    packet = sr1(IP(dst=target_ip)/TCP(sport = src_port, dport=port, flags='S'), timeout=1, verbose=0) # TCP packet with SYN flag.

    if packet != None:
        if packet.haslayer(TCP):
            if packet[TCP].flags == SYN_ACK:
                rst_packet = IP(dst=target_ip)/TCP(sport=src_port, dport=port, flags='R') # Ending the connection (stealth), TCP packet with RST flag
                sr1(packet, timeout=1, verbose=0)
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


def clear_button_function(results_text):
    results_text['state'] = 'normal'
    results_text.delete('1.0', END)
    results_text['state'] = 'disabled'


def start_button_function(target_ip_entry, min_port_entry, max_port_entry, results_text):           
    target_ip = target_ip_entry.get()
    try:
        min_port = int(min_port_entry.get())
        max_port = int(max_port_entry.get())

    except Exception:
            results_text['state'] = 'normal'
            results_text.insert(END, '[~] ERROR, Invalid Ports\n')
            results_text['state'] = 'disabled'               
            return False         
    
    target_ip_entry.delete(0, 'end')
    min_port_entry.delete(0, 'end')
    max_port_entry.delete(0, 'end')  
    
    
    if min_port >= 0 and max_port >=0 and max_port >= min_port:
            pass
    else:
            results_text['state'] = 'normal'
            results_text.insert(END, '[~] ERROR, Invalid Range of Ports\n')
            results_text['state'] = 'disabled'                
            return  False   
    
    state = check_host(target_ip, results_text)             
    if state == False:
        return False

    ports = range(int(min_port), int(max_port) + 1)           
    result = ''

    results_text['state'] = 'normal'  
    results_text.insert(END, '[!] Scanning Started...' + '\n')
    results_text['state'] = 'disabled'      
    for port in ports:        
        status = syn_port_scan(port, target_ip)
        if status == 'OPN':
            result = 'Port ' + str(port) + ' -> OPEN'                   
        elif status == 'CLS':
            result = 'Port ' + str(port) + ' -> CLOSED'                  
        elif status == 'F':
            result = 'Port ' + str(port) + ' -> FILTERED'                  
        elif status == 'UNK':
            result = 'Port ' + str(port) + ' -> UNKNOWN'                  
        else:
            result = 'Port ' + str(port) + ' -> UNANSWERED'                

        results_text['state'] = 'normal'  
        results_text.insert(END, result + '\n')
        results_text['state'] = 'disabled'           


def main():
    root.geometry('500x260')
    root.title('PORT SCAN (SYN)')   

    # Port Scanner Interface
    target_ip_label = Label(root, text='TARGET IP:')
    target_ip_label.grid(row=0, column=0)    
    target_ip_entry = Entry(root, width=40)
    target_ip_entry.grid(row=0, column=1)

    min_port_label = Label(root, text='MIN PORT:')
    min_port_label.grid(row=1, column=0)    
    min_port_entry = Entry(root, width=40)
    min_port_entry.grid(row=1, column=1)

    max_port_label = Label(root, text='MAX PORT:')
    max_port_label.grid(row=2, column=0)    
    max_port_entry = Entry(root, width=40)
    max_port_entry.grid(row=2, column=1)       

    results_label = Label(root, text='RESULTS')
    results_label.grid(row=4, column=0)        
    results_text = Text(root, height=8, width=40, state='disabled')
    results_text.grid(row=4, column=1)    
    
    clear_button = Button(root, text='CLEAR', command=lambda: clear_button_function(results_text), fg='black', bg='lightgreen')
    start_button = Button(root, text='START', command=lambda: threading.Thread(target=start_button_function, args=(target_ip_entry, min_port_entry, max_port_entry, results_text)).start(), fg='black', bg='lightgreen')
    start_button.grid(row=5, column=0, padx=10, pady=5)
    clear_button.grid(row=5, column=1, padx=10, pady=5)  

    root.mainloop()


if __name__ == '__main__':
    main()