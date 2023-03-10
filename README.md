## Cybersecurity Tools with Python

### What does it do?
Implementation of three tools in Python using the Scapy library: Port scanner, Sniffer and DOS simulator. The tools run specificaly in unix-based systems, all tests were done using virtual machines with VirtualBox NAT network environments.


### How to Use?
#### Clone the Repository
```bash
$ git clone https://github.com/alexandreclem/CyberTools-with-Python.git
```
#### Dependencies
- Scapy Library
    - Run:
        ```bash
        $ python -m pip install scapy
        ```
- Tkinter Library
    - Run:
        ```bash
        $ python -m pip install tk
        ```
#### Tests Scenarios
- Virtualized Environment using VirtualBox
    - NAT Network
        - IP - 10.0.2.0/24
        - xubuntu_1 - IP 10.0.2.5 / Interface enp0s9 (Attacker)
        - xubuntu_2 - IP 10.0.2.4 / Interface enp0s9
        - xubuntu_2 - Apache Server in the 80 port

<p align="center" width="100%">
    <img width="100%" src="https://raw.githubusercontent.com/alexandreclem/CyberTools-with-Python/master/images/1.png">    
</p>

- Give execution permission to all directories
    - Within the **src** directory, run:
        ```bash
        $ sudo chmod -R 777 ./dos
        $ sudo chmod -R 777 ./port_scan
        $ sudo chmod -R 777 ./sniffing
        ```
- DOS
    - Within the **src/dos** directory, run:
        ```bash
        $ sudo ./dos.py
        ```
    
<p align="center" width="100%">
    <img width="100%" src="https://raw.githubusercontent.com/alexandreclem/CyberTools-with-Python/master/images/3.png">    
</p>

- Port Scanner
    - Within the **src/port_scan** directory, run:
        ```bash
        $ sudo ./port_scan.py
        ```
<p align="center" width="100%">
    <img width="100%" src="https://raw.githubusercontent.com/alexandreclem/CyberTools-with-Python/master/images/2.png">    
</p>

- Sniffing
    - Within the **src/sniffing** directory, run:
        ```bash
        $ sudo ./sniffing.py
        ```
<p align="center" width="100%">
    <img width="100%" src="https://raw.githubusercontent.com/alexandreclem/CyberTools-with-Python/master/images/4.png">    
</p>
<p align="center" width="100%">
    <img width="100%" src="https://raw.githubusercontent.com/alexandreclem/CyberTools-with-Python/master/images/5.png">    
</p>


