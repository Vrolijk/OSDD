Working with UDPCast to transfer files made me wonder is there is an other application to create a one way tunnel that has the Forward Error Control (FEC) functionality combined with rate limiting.

If there is no application this could be an idea for a hackaton or a development team.

In my opionion the software should contain a sender and receiver that is able to recieve data from a variation of applications.
The goal is to create a permanent uni-directional tunnel between 2 computers
<img src="img/netcat-diode.png" width=300>


Sender
a) should run constantly waiting for input from an application like a NETCAT tunnel (ref 1)
b) should be able to configure the transfer speed
c) should send a keep alive every X receiver
d) should add a sequencenumber to each packet
e) could log a manifest on the senders machine
f) could send the manifest every X to the receiver
g) should be able to send to an IP, broadcast address or multicast destionation on a specific interface
h) should be able to add Forward Error Control (FEC) like UDPcast (ref 2)
g) could be able to cache packets with a configurable disklocation and size
h) could be able to add encryption using a defined password of public/priavte key
i) should send every message/file/object as a separate session (to prevent the tunnel to terminate when one session fails)
j) should be able to run as an application or a service 
k) could be able to run a speed optimization to determine optiomal speed and settings

Receiver
a) should run constantly waiting for input from a sender like a NETCAT tunnel (ref 1)
b) should listen for a keep alive every X from the sender
c) should monitor the packet sequencenumber and report on missing packets and report on missing packets
d) could be able to receive a manifest and report on missing items
e) could be able to log and report on missing sequencenumbers 
f) could be able to add encryption using a defined password of public/private key
g) should be able to run as an application or a service 
h) could be able to run a speed optimization to determine optiomal speed and settings and advice optimal settings

ref 1: https://www.devkb.org/linux/115-TCP-tunnel-port-forwarding-using-Netcat 
ref 2: https://github.com/elisescu/udpcast/blob/master/fec.c
