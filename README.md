# Simple data-diode proxy examples

## Workshop working with data diodes
[Click here for the workshop](workshop/readme.md)

## Packet loss (almost) explained
[Packet loss explained](packetloss_explained.md)

## Example data-diode hardware setups
[Datadiode hardware setups](datadiode_hardware_setups.md) <br>
Extra: [€25 euro functional data-diode demonstrator](https://github.com/Vrolijk/OSDD/blob/main/examples/25_euro_data-diode_demonstator.md)

## Send large file or multiple files data-diode using UDPcast: 

In this example we will show how to send one or multiple files trough a data-diode using UDPCAST on Linux. UDPcast is also available for Windows. For more information about UDPcast see http://www.udpcast.linux.lu/

For this example we used 2 proxies with a gigabit data-diode in the middle. <br>
Configure the senders network interface connected to the data-diode to 10.0.0.1, subnet 255.255.255.0 and gateway. <br>
Configure the receivers network interface connected to the data-diode to 10.0.0.2, subnet 255.255.255.0 and gateway.

<img src="img/img_simple_datadiode_setup.png" width=300>

### Create a 5Gb file

**Create random file of 5Gb**

```head -c 5120M /dev/urandom > 5gb-testfile.tmp```

### Transfer single 5Gb file

UDPCAST sends data using UDP and has the possibility to send the data over unidirectional connections like radio. It also adds the possibility to add FEC (Forward Error Correction) and to limit the transfer speed. This makes UDPcast an ideal tool to send data trough a data-diode.

*all items between \<\<variable\>\> are variables and can be found in the application man pages.*

Receiver: 

```udp-receiver --nosync --interface <<enp0s3>> --file 5gb-testfile.tmp```

Sender: 

```udp-sender --interface <<enp0s8>> --async --fec <<8x8/64>> --max-bitrate <<600Mbps>> --file 5gb-testfile.tmp --broadcast --rexmit-hello-interval 1000 --autostart  3```

### validate received file using sha256sum

On both proxies the outcome should be identical: 

```sha256sum 5gb-testfile.tmp```



## Send multiple files or directories

Sending large and multiple files trough a data-diode / unidirectional network connection using udpcast and tar.

Receiver:

```udp-receiver --nosync --interface enp0s3 | tar –x```

Sender: 

```tar -c <</data/>> | udp-sender --interface <<enp0s8>> --async --fec 8x8/64 --max-bitrate <<600Mbps>> --broadcast --autostart 3 --rexmit-hello-interval 1000  --nokbd ```

## Tail files using netcat

For sending data directly to an IP address first we need to add an arp entry at the sender. To simplify this we use a layer 2 broadcast address. Please note that sending data to fast can cause packet loss and netcat will crash.

```sudo arp -i <<enp0s8>> -s <<10.0.0.2>> ff:ff:ff:ff:ff:ff```
  
Receiver:
  
```nc -l -u -p 9999 >> /tmp/netcat.log```

Sender 

```tail -F /var/log/syslog | nc -u <<10.0.0.2>> 9999```
  
  
## Send audio or video stream using VLC media player

Receiver:

Open VLC media player and go to

``` Media-> open network stream -> network url rtp://@:5004 ``` 

Sender:

First make sure your sender knowns the correct interface to send the data with an ARP inject.

```sudo arp -i <<enp0s8>> -s <<10.0.0.2>> ff:ff:ff:ff:ff:ff```

Open VLC media player and go to

``` Media -> stream -> <<choose source: example http://icecast.omroep.nl/radio4-bb-mp3>> -> Stream button-> next -> new destination -> RTP / MPEG transport stream -> add -> address <<10.0.0.2>> base Port 5004 stream name <<OSDD>> -> next -> profile Video - H264 + mp3 (mp4) -> next -> stream ```

It takes a few seconds to start the video on the receiver because of caching.

For more Dutch sources: https://mediamagazine.nl/live-links-nederland/livestreams-nederland-landelijk/  
  
## Possibilities for tweaking

UDP buffers to 32Mb.
```
net.core.rmem_max = 32777216
net.core.rmem_default = 32777216
net.core.wmem_max = 32777216 
net.core.wmem_default = 32777216
net.core.netdev_max_backlog = 100000
```

Set MTU on all to the OSDD connected interfaces to jumbo frames. No impact on UDPCAST due to fixed maximum packet size but will be useful for other applications. 

```ifconfig <<enp0s3>> mtu 9000```

# Links

## UDPcast as a service

https://github.com/azzid/pmddft
