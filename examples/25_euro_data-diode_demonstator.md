# €25,- COTS data-diode demonstrator

WARNING THIS IS NOT A REAL DATA-DIODE! It's just for educational purposes. <br>
<i>If it looks like a duck, swims like a duck, and quacks like a duck, in this case it's not a duck.</i>

To be able to work with data-diodes it helps to have a cheap way of simulating a hardware data-diode. With a €25,- managed switch it's possible to create a 
data-diode for development purposes. <br>
Please note: this does not provide the same security as a real data-diode since the configuration could be modified to support bi-directional traffic!

## Step 1: Buy a €25,- TP-link TL-SG105e managed switch. 
This can be done with most managed switches that support vlans and port mirroring. We choose the TP-link for the price and easy availability. <br>
Connect the switch directly to your PC and change your IP for the connected interface manually to 192.168.0.2. Open your browser and go to the (default) IP from the TP-link http://192.168.0.1. UserID/Password is admin/admin.<br> 

<img src="/img/tp-link_hardware.jpg" width=300>

## Step 2: Modify vlan per port settings
Go to the menu VLAN -> Port Based VLAN. <br>
- Enable Port Based VLAN-Configuration
- Add VLAN ID 2 and select port 1 and press apply
- Add VLAN ID 5 and select port 5 and press apply
- It's possible to assign every port their own VLAN but this is a more advanced use-case.

<img src="/img/TP-link_switch_vlan_settings.png" width=400>

## Step 3: Modify port mirror
Go to the menu Monitoring -> Port Mirror
- Port Mirror: select enable, mirroring Port select Port 5
- At Mirrored Port select Port 1 (2 -3 is also possible), Ingress select enable, Egress select Disable
- Press Apply
<img src="/img/TP-link_switch_port_mirror_settings.png" width=400>

## Step 4: Disable DHCP 
By default DHCP is enabled to provide access to the web based management interface. We want to disable DHCP to prevent the switch asking for DHCP servers which generates traffic.<br>
This can also be abused by hackers to identify the management IP and modify the setting back to bi-directional traffic.
Go to the menu System -> IP Setting
- IP Address Setting, DHCP setting select Disable
- You could change the IP but this is not needed.

<img src="/img/TP-link_switch_dhcp_settings.png" width=400>

## Step 5: Disable TP-link loop prevention
TP-Link has a feature that prevents loops in the network. This feature creates traffic and we don't want that on a data-diode. 
Go to the menu Monitoring, Loop Prevention
- Select Disable
- Press Apply

<img src="/img/TP-link_switch_loop_prevention_settings.png" width=400>

## Step 6: Enjoy your data-diode for development purposes 
- Connect your TX proxy to interface 1 
- Connect your RX proxy to interface 5

Enjoy your data-diode demonstrator. 

<img src="/img/img_simple_datadiode_setup.png" width=300>

## Simple trouble shooting
- Manually change the TX and TX proxy IP addresses in the same range and disable IPv6
- Do not forget the ARP injection on the TX proxy when sending traffic directly to the RX proxy
- Run TCPDump on both the TX and RX proxies to validate packets are sent and received.

## Do not use in production!!!
Since we are limiting the functionality of bidirectional by VLAN separation and port mirroring its still possible for an attacker to access the web interface on the switch. <br>
A real data-diode doesn't have any function for bi-directional traffic.
Example how to hack the TP-Link: https://www.pentestpartners.com/security-blog/how-i-can-gain-control-of-your-tp-link-home-switch/
