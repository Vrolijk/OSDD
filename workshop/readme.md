# Securing Your Network: A Hands-On Workshop on Data Diodes and Proxies
Welcome to this exciting workshop on the basics of data diodes and proxies. Over the next few hours, we will be diving into the world of network security and learning how to use two laptops named PING and PONG, a data diode, and proxies to secure data communication.

Throughout the workshop, we will be working with Ubuntu and learning how to update the operating system, change IP settings, and manipulate the ARP table. Additionally, we will test the connection from laptop PING to PONG and install software to start three different data streams through the data diode.

By the end of the workshop, you will have a strong understanding of data diodes and proxies, and how they can be used to enhance network security. So, let's get started and dive into the exciting world of network security!

<b> CAUTION: WORK IN PROGRESS!! </b>

# Data diode basics and problems
![Communication layers](/img/TCP-IP-model-vs-OSI-model.png) <br>


![Overview packet loss](/img/datadiode_packetloss.png) <br>
1: The application/script needs to support uni-directional communication. UDP is the most common protocol to use.<br>
2: At the kernel UDP is a low priority and packets can be dropped. See footnote[^1] <br>
3: Depending on the speed of the data diode we didn't found any packet drops with the TP-Link switch<br>
4: At the kernel UDP is a low priority and packets can be dropped. See footnote[^1] <br>
5: Packets are send to the application. Depending on your hardware there could be a processing or disk IO write issue. <br>
6: If you send data directly to the IP address of RX/PONG machine you need to add an ARP inject on TX/PONG 

# Setup 
## step 1: Prepare the data diode
If not allready prepared follow the instructions on https://github.com/Vrolijk/OSDD/blob/main/examples/25_euro_data-diode_demonstator.md <br>
Connect PING to the IN (port 1) and PONG to OUT (port 5) connection.<br>
<< TO DO ADD PHOTO >>

## Step 2: Change the IP settings
PING: Change the IP to 10.0.0.1 with subnet 255.255.255.0 <br>
PONG: Change the IP to 10.0.0.2 with subnet 255.255.255.0 <br>
<< TO DO ADD PHOTO >> <br>

* Open <b>tcpdump</b> on both machines on the interface connected to the data diode <br>
```sudo tcpdump -i enp1s0```
* Ping 10.0.0.2 from TX/PING
* Note that on PONG there is an ARP reply <br>
``` << add tcpdump example >> ``` <br>
On PING you only see the request, not the reply

## Step 4: Add ARP entry to TX/PING
First install net-tools <br>
```sudo apt install net-tools -y``` <br>
To tell PING that PONG 'lives' behind interface enp1s0 add the following ARP entry. <br>
```sudo arp -i enp1s0 -s 10.0.0.2 ff:ff:ff:ff:ff:ff``` <br>
Note that we are broadcasting the packets to ff:ff:ff:ff:ff:ff. You could also add the mac address of PONG here.<br>
Now ping PONG again. You notice that there is no more ARP reply on PONG. <br>
``` << add tcpdump example >> ``` <br>
## Step 5: Netcat hello world
On PONG start: <br>
```nc -l -u -p 9999```

Then start on PING: <br>
```echo "Hello world | nc -u <<10.0.0.2>> 9999```



Futher reading:
[^1]: https://blog.cloudflare.com/how-to-receive-a-million-packets/ 
