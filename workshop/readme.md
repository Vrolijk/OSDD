# Securing Your Network: A Hands-On Workshop on Data Diodes and Proxies
Welcome to this exciting workshop on the basics of data diodes and proxies. Over the next few hours, we will be diving into the world of network security and learning how to use two laptops named PING and PONG, a data diode, and proxies to secure data communication.

Throughout the workshop, we will be working with Ubuntu and learning how to update the operating system, change IP settings, and manipulate the ARP table. Additionally, we will test the connection from laptop PING to PONG and install software to start three different data streams through the data diode.

By the end of the workshop, you will have a strong understanding of data diodes and proxies, and how they can be used to enhance network security. So, let's get started and dive into the exciting world of network security!

<b> CAUTION: WORK IN PROGRESS!! </b>

# Target 

# Data diode basics and problems
Position of the data diode in the security landscape 

<img src="/img/datadiode_position_security_landscape.png" width="600"> <br>
And Cross Domain Solutions.. <br>

High level overview of the network connection layers 

<img src="/img/TCP-IP-model-vs-OSI-model.png" width="300"> <br>
And the data layer. If we want to prevent data leakage we need to filter on the data level. This makes the data diode not only a network solution but combines all layers including the content (layer 8?).

Data and packet flow explained

<img src="/img/datadiode_packetloss.png" width="600"> <br>
1: The application/script needs to support uni-directional communication. UDP is the most common protocol to use.<br>
2: At the kernel UDP is a low priority and packets can be dropped. See footnote[^1] <br>
3: Depending on the speed of the data diode we didn't found any packet drops with the TP-Link switch<br>
4: At the kernel UDP is a low priority and packets can be dropped. See footnote[^1] <br>
5: Packets are send to the application. Depending on your hardware there could be a processing or disk IO write issue. <br>
6: If you send data directly to the IP address of RX/PONG machine you need to add an ARP inject on TX/PONG 

***
# Setup 
## step 1: Prepare the data diode
If not already prepared follow the instructions on [€25,- data diode demonstrator](https://github.com/Vrolijk/OSDD/blob/main/examples/25_euro_data-diode_demonstator.md) <br>

Connect PING to the IN (port 1) and PONG to OUT (port 5) connection.<br>
<img src="/img/datadiode_workshop_setup.png" width="600"> <br>

## Step 2: Change the IP settings
PING: Change the IP to 10.0.0.1 and subnet 255.255.255.0 <br>
PONG: Change the IP to 10.0.0.2 and subnet 255.255.255.0 <br>
<img src="/img/datadiode_workshop_ip.png" width="600"> <br>
We advice to reboot after this step. <br>

## Step 3 Possibilities for tweaking

Increase UDP buffers to 32Mb. This is needed after every reboot.
```
sudo sysctl -w net.core.rmem_max=32777216
sudo sysctl -w net.core.rmem_default=32777216
sudo sysctl -w net.core.wmem_max=32777216 
sudo sysctl -w net.core.wmem_default=32777216
```

## Step 4: monitoring
**tcpdump** 
* Open <b>tcpdump</b> on both machines on the interface connected to the data diode <br>
```sudo tcpdump -i enp1s0```
* Ping 10.0.0.2 from TX/PING
* Note that on PONG there is an ARP reply <br>
```1c:6f:65:4f:54:6b > ff:ff:ff:ff:ff:ff, ARP, length 42: Request who-has 10.0.0.2 (ff:ff:ff:ff:ff:ff) tell 192.168.1.3, length 28 ```
```1c:6f:65:4d:bb:98 > 1c:6f:65:4f:54:6b, ARP, length 60: Reply 10.0.0.2 is-at 1c:6f:65:4d:bb:98, length 46 ```
  <br>
On PING you only see the request, not the reply. <br>
This is the most common problem when working with data diodes. <br>

## Step 5: Add ARP entry to TX/PING
To tell PONG that 10.0.0.2 lives on enp1s0 add an ARP entry. This is needed after every reboot. <br><br>

First install net-tools <br>
```sudo apt install net-tools -y``` <br>
To tell PING that PONG 'lives' behind interface enp1s0 add the following ARP entry. <br>
```sudo arp -i enp1s0 -s 10.0.0.2 ff:ff:ff:ff:ff:ff``` <br>
Note that we are broadcasting the packets to ff:ff:ff:ff:ff:ff. You could also add the mac address of PONG here.<br><br>
Now ping PONG again. You notice that there is no more ARP reply on PONG. <br>
``` << add tcpdump example >> ``` <br>

## Step 6: Netcat hello world
On PONG start: <br>
```nc -l -u -p 9999```

Then start on PING: <br>
```echo "Hello world" | nc -u 10.0.0.2 9999```

## Step 7: Send large files using UDPCAST
UDPCAST sends data using UDP and has the possibility to send the data over unidirectional connections like radio. It also adds the possibility to add FEC (Forward Error Correction) and to limit the transfer speed. This makes UDPcast an ideal tool to send data trough a data-diode.

**Create random file of 1Gb**

```head -c 1024M /dev/urandom > 1gb-testfile.tmp```

**send the file**

On PONG: 

```udp-receiver --nosync --interface enp1s0 --file 1gb-testfile.tmp```

On PING: 

```udp-sender --interface enp1s0 --async --fec 8x8/64 --max-bitrate 600Mbps --file 1gb-testfile.tmp --broadcast --rexmit-hello-interval 1000 --autostart  3```

**Validate received file using sha256sum**

On both proxies the outcome should be identical: 

```sha256sum 1gb-testfile.tmp```

## Step 8: Send audio or video stream using VLC media player

PONG:

Open VLC media player and go to

``` Media-> open network stream -> network url rtp://@:5004 ``` 

PING:

Open VLC media player and go to

``` Media -> stream -> <<choose source: example http://icecast.omroep.nl/radio4-bb-mp3>> -> Stream button-> next -> new destination -> RTP / MPEG transport stream -> add -> address 10.0.0.2 base Port 5004 stream name OSDD -> next -> profile Video - H264 + mp3 (mp4) -> next -> stream ```

It takes a few seconds to start the video on the receiver because of caching.

For more Dutch sources: https://mediamagazine.nl/live-links-nederland/livestreams-nederland-landelijk/  
  
## Step 9: Netcat pipe large file (fails)
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

**ss network queue**

Open on both machines in a seperate terminal to monitor the UDP queue on destionation port 9999. Still need to test<br>
``` watch -n 1 "ss -u -a -p -t '( dport = :9999 )'" ``` 

***
Futher reading:
[^1]: https://blog.cloudflare.com/how-to-receive-a-million-packets/ 
