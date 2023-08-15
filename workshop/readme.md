# Securing Your Network: A Hands-On Workshop on Data Diodes and Proxies
Welcome to this workshop on the basics of data diodes and proxies. Over the next few hours, we will be diving into the world of network security and learning how to use two laptops named PING and PONG and a data diode to setup a unidirectional data communication path.

Throughout the workshop, we will be working with 2 Ubuntu computers to learn how to update the operating system configuration, change IP settings, and manipulate the ARP table. Additionally, we will test the connection from laptop PING to PONG and install software to start three different data streams through the data diode.

By the end of the workshop, you will have a strong understanding of data diodes and proxy software, and how they can be used to enhance network security. So, let's get started and dive into the exciting world of network security!

<b> This workshop is still under development, feedback and improvements are more than welcome </b>

## step 1: Prepare the data diode
For this workshop we will use 2 standard laptops with an ethernet port, OS latest LTS Ubuntu and a TP-link TL-SG105e managed switch configured as a (functional) data diode. Any other data diode will work. <br> 
If the TP-link isn't already prepared follow the instructions on [€25,- data diode demonstrator](https://github.com/Vrolijk/OSDD/blob/main/examples/25_euro_data-diode_demonstator.md) <br>

Connect laptop PING to the IN (port 1) and laptop PONG to OUT (port 5) connection.<br>
<img src="/img/datadiode_workshop_setup.png" width="600"> <br>

## Step 2: Change the IP settings
Laptop PING: Change the IP to 10.0.0.1 and subnet 255.255.255.0 <br>
Laptop PONG: Change the IP to 10.0.0.2 and subnet 255.255.255.0 <br>
<img src="/img/datadiode_workshop_ip.png" width="600"> <br>
If needed enlarge the image and follow step 1 to 5 (Numbers in red)

## Step 3 Possibilities for tweaking

Since UDP is a low priority protocol the Linux kernel can, and will, drop packet on PING and PONG. <br>
!! This is one of the main reasons of packetloss when working with data diodes, not the data diode itself.<br>
See [Packetloss explained](https://github.com/Vrolijk/OSDD/blob/main/packetloss_explained.md) for a more in depth explanation. 

Increase UDP buffers to 32Mb. This is needed after every reboot.
```
sudo sysctl -w net.core.rmem_max=32777216
sudo sysctl -w net.core.rmem_default=32777216
sudo sysctl -w net.core.wmem_max=32777216 
sudo sysctl -w net.core.wmem_default=32777216
sudo sysctl -w net.core.netdev_max_backlog=100000
```
### Or permanently increase the UDP queue sizes.
To make the udp buffer change permanent you need to edit /etc/sysctl.conf file on both machines and put following lines so that after reboot the setting will remain as it is:  <br>
Open a terminal and run the command: <br>
```sudo gedit /etc/sysctl.conf```

Append a config directive as follow at the end of the file, save and close the document:
```
net.core.rmem_max = 32777216
net.core.rmem_default = 32777216
net.core.wmem_max = 32777216 
net.core.wmem_default = 32777216
net.core.netdev_max_backlog = 100000
```
## Step 4: Test connection and fail on ARP resolution
**tcpdump** 
* Open <b>tcpdump</b> on both laptops on the interface connected, often enp1s0, to the data diode <br>
```sudo tcpdump -i enp1s0```
* In a new terminal op laptop PING run the application ping to test the connection to PONG <br>
```ping 10.0.0.2```
* Note that on PONG tcpdump shows is an ARP reply <br>
```ab:6f:65:bb:54:6b > ff:ff:ff:ff:ff:ff, ARP, length 42: Request who-has 10.0.0.2 (ff:ff:ff:ff:ff:ff) tell 10.0.0.1, length 28 ```
```ab:6f:65:bb:bb:98 > ab:6f:65:bb:54:6b, ARP, length 60: Reply 10.0.0.2 is-at ab:6f:65:bb:bb:98, length 46 ```
  <br>

On PING you only see the <b>Request who-has</b>, not the reply. This is the most common problem when working with data diodes because PING has no information about PONG. PONG tries to inform PING but the data diode blocks the reply. In the next step we will manually supply this information to PING. <br>

Remember: For troubleshooting data diodes using <b>tcpdump</b> on both machines is the first thing to do. Check if you see traffic on both machines, check for ARP replies on PONG. Next to packet loss this is a common issue that is often overlooked. Now let's fix this in step 5.

## Step 5: Add ARP entry to PING laptop
To tell PING that 10.0.0.2 is behind the interface enp1s0 we need to add an ARP entry. This is needed after every reboot or you can make the entry permanent. <br>

First install net-tools on PING <br>
```sudo apt install net-tools -y``` <br>
To tell PING that PONG 'lives' behind interface enp1s0 add the following ARP entry. <br>
```sudo arp -i enp1s0 -s 10.0.0.2 ff:ff:ff:ff:ff:ff``` <br>
Note that we are broadcasting the packets to ff:ff:ff:ff:ff:ff. You could also add the mac address of PONG here.<br><br>

Now ping PONG again from PING. You notice on laptop PONG that there is no more ARP but shows ICMP reply.PING will not receive the echo reply.<br>
``` 14:59:48.026559 IP 10.0.0.1 > 004: ICMP echo request, id 2, seq 1, length 64 ``` <br>
 ```14:59:48.026607 IP 004 > 10.0.0.1: ICMP echo reply, id 2, seq 1, length 64 ``` 

### Optional: make the ARP entry permanent on PING
Run the following command to create a startup script. This way you will not forget to add the ARP entry after a reboot. You need to install net-tools to add the application Arp.
```
sudo gedit /etc/rc.local
```
Add the following:
```
#!/bin/bash
arp -i enp1s0 -s 10.0.0.2 ff:ff:ff:ff:ff:ff 
exit 0
```
Save and close gedit and run from the terminal
```
sudo chmod +x /etc/rc.local
```
Reboot

# Preparations are done, now let's start with the 3 examples.
## Use case 1: Simple message using Netcat "Hello world"
On laptop PONG open a terminal and start: <br>
```nc -l -u -w 1 -p 9999```

Then start on PING: <br>
```echo "Hello world" | nc -u -w 1 10.0.0.2 9999```

This is a very simple example to test the data diode. Please remember to start the laptop PONG, the receiver, first. By sending just a small message in most cases there is no problem with [packetloss](https://github.com/Vrolijk/OSDD/blob/main/packetloss_explained.md).

## Use case 2: Send large files using UDPCAST
UDPCAST sends data using UDP and has the possibility to send the data over unidirectional connections like radio. It also adds the possibility to add FEC (Forward Error Correction) and to limit the transfer speed. This makes UDPcast an ideal tool to send data through a data-diode.

First install udpcast on PING and PONG <br>
```sudo apt install udpcast -y``` <br>


**Create random file of 1Gb**

```head -c 1024M /dev/urandom > 1gb-testfile.tmp```

**send the file**

On PONG: 

```udp-receiver --nosync --interface enp1s0 --file 1gb-testfile.tmp```

On PING: 

```udp-sender --interface enp1s0 --async --fec 8x8/64 --max-bitrate 600Mbps --file 1gb-testfile.tmp --broadcast --rexmit-hello-interval 1000 --autostart  3```

**Validate received file using sha256sum**


Open a terminal on PING and PONG and start the following command. On both proxies the sha256 hash should be identical. 

```sha256sum 1gb-testfile.tmp``` <br> <br> 
It often happens that after starting udpcast for the first time PONG stops receiving data before the transfer is done. We assume this is due to how Linux handles the udp queue that results in [packetloss](https://github.com/Vrolijk/OSDD/blob/main/packetloss_explained.md). When you restart the Udpcast commands on both laptops it will often work. <br> <br>
<< to do: add udp-sender screen when the session is not complete >> <br> 

## Use case 3: Send audio or video stream using VLC media player

First install vlc on PING and PONG <br>
```sudo apt install vlc -y``` <br>


PONG:

Open VLC media player and go to

``` Media-> open network stream -> network url rtp://@:5004 ``` 

PING:

Open VLC media player and go to

``` Media -> stream -> https://stream.qmusic.nl/fouteuur/mp3 -> Stream button-> next -> new destination -> RTP / MPEG transport stream -> add -> address 10.0.0.2 base Port 5004 stream name OSDD -> next -> profile Video - H264 + mp3 (mp4) -> next -> stream ```

It takes a few seconds to start the video on the receiver because of caching. <br>
For a videostream use: ```https://live-hls-web-aje.getaj.net/AJE/05.m3u8``` <br>
For more Dutch radio genres: ```https://mediamagazine.nl/live-links-nederland/livestreams-nederland-landelijk/``` 
<br><br>
# End of the workshop! :)

# Open items, help appreciated to test and improve ##

## Send multiple files or directories

Sending large and multiple files through a data-diode / unidirectional network connection using udpcast and tar.

Receiver:

```udp-receiver --nosync --interface enp1s0 | tar –x```

Sender: 

```tar -c /data-directory/ | udp-sender --interface enp1s0 --async --fec 8x8/64 --max-bitrate 600Mbps --broadcast --autostart 3 --rexmit-hello-interval 1000  --nokbd ```


## Tail files using netcat

<b>On PONG</b>

Terminal 1: create a file called /tmp/netcat.log

```touch /tmp/netcat.log```

Tail (Open the file and wait for new data) /tmp/netcat.log

```tail -f /tmp/netcat.log```

Terminal 2: Start the netcat listener and add the data to /tmp/netcat.log

```nc -l -u -p 9999 >> /tmp/netcat.log```

<b>On PING</b>

Read the syslog file and send it to PONG on port 9999

```tail -F /var/log/syslog | nc -u 10.0.0.2 9999```

Now open an application like firefox and close it. You should see the data on the second terminal on PONG.




## Monitor packetloss using ss network queue

Open on both machines in a separate terminal to monitor the UDP queue on destination port 9999. Still need to test<br>
``` watch -n 1 "ss -u -a -p -t '( dport = :9999 )'" ``` 



## Force network queue to drop packets: Netcat pipe large file
On PONG start: <br>
```nc -l -u -p 9999 > 1gb-testfile.tmp```

Then start on PING: <br>
```cat 1gb-testfile.tmp | nc -u 10.0.0.2 9999```


Probably this went wrong. Try to reduce the speed with PipeViewer PV. <br>
On PONG start: <br>
```nc -l -u -p 9999 > 1gb-testfile.tmp```

Then start on PING: <br>
```sudo apt install pv```
<br>
```cat 1gb-testfile.tmp | pv -L 30m | nc -u 10.0.0.2 9999```
<br><br><br><br>

# Data diode basics and problems
The data diode isn't the solution for all your problems. Here is an overview of the various ways to bridge 2 networks. <br><i>Note: This overview misses the Cross Domain Solutions (CDS). </i><br>

<img src="/img/datadiode_position_security_landscape.png" width="600"> <br>


This is a high level overview of the network connection layers. The data diode will only allow data from A to B. This will break a lot protocols on all OSI layers because handshakes and validations will not work. Example: The TCP protocol first checks the connection by sending a SYN packet, the receiving computer will receive the packet but the diode stops the ACK reply. Since UDP is stateless, no handshake needed, we will use this protocol in most use-cases.

<img src="/img/TCP-IP-model-vs-OSI-model.png" width="300"> <br>


If we want to prevent data leakage from the TX proxy to the RX proxy need to add filters and policies on the sending and/or receiving proxies. The data diode just forwards all packets and doesn't care about the content of the packets.<br> 
TThis makes the data diode not only a network solution but we need some extra work to add protection on all OSI layers including the user and content (OSI layer 8 and 9?) by including filtering and processes.<br>
<img src="/img/img_simple_datadiode_setup.png" width="300"> <br>


***
Futher reading:
[^1]: https://blog.cloudflare.com/how-to-receive-a-million-packets/ 

[^2]: https://alibaba-cloud.medium.com/analysis-of-udp-packet-loss-problem-in-linux-system-a5b6bd59d97b
