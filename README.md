# Simple datadiode examples

## Send single large file and multiple files datadiode test using UDPcast: 

In this example we will show how to send one or multiple files trough a datadiode using UDPCAST using Linux. UDPcast is also available for Windows. For more information about UDPcast see http://www.udpcast.linux.lu/

For this example we used 2 proxies with a gigabit datadiode in the middle. 

## Create a 5Gb file

**Create random file of 5Gb**

```head -c 5120M /dev/urandom > 5gb-testfile.tmp```

## Transfer single 5Gb file

**Transfer using udpcast trough datadiode with different parameters**

*all items between \<\<variable\>\> are variables and can be found in the application man pages.*

Sender: 

```udp-sender --interface <<enp0s8>> --async --fec <<8x8/128>> --max-bitrate <<600Mbps>> --file 5gb-testfile.tmp –broadcast```

Receiver: 

```udp-receiver –nosync –interface <<enp0s3>> --file 5gb-testfile.tmp```

**validate received file using sha256sum**

On both proxies the outcome should be identical: 

```sha256sum 5gb-testfile.tmp```



## Send multiple files or directories

Sending large and multiple files trough a datadiode / unidirectional network connection using udpcast and tar

Receiver:

```udp-receiver --nosync --interface enp0s3 | tar –x```

Sender: 

```tar -c /data/ | udp-sender --interface <<enp0s8>> --async --fec 8x8/64 --max-bitrate 800Mbps --broadcast --autostart 1 --nokbd ```

## Tail files using netcat

For sending data directly to an IP address first we need to add an arp entry at the sender. To simplefy this we use a layer 2 broadcast address. Please note that sending data to fast can cause packetloss and netcat will crash.

```sudo arp -i <<enp0s8>> -s <<192.168.1.2>> ff:ff:ff:ff:ff:ff```
  
Receiver:
  
```nc -l -u -p 9999 >> /tmp/netcat.log```

Sender 

```tail -F /var/log/syslog | nc -u <<192.168.1.2>> 9999```
  
  
## Send audio or video stream using VLC mediaplayer

Receiver:

Open VLC mediplayer and go to

``` Media-> open network stream -> network url rtp://@:5004 ``` 

Sender:

Open VLC mediaplayer and go to

``` Media -> stream -> <<choose source: example http://icecast.omroep.nl/radio4-bb-mp3>> -> Stream button-> next -> new destination -> RTP / MPEG transport stream -> add -> address <<192.168.1.2>> base Port 5004 stream name <<OSDD>> -> next -> profile Video - H264 + mp3 (mp4) -> next -> stream ```

It takes a few seconds to start the video on the receiver because of caching.

For more Dutch sources: https://mediamagazine.nl/live-links-nederland/livestreams-nederland-landelijk/  
  
## Possibilities for tweaking

UDP buffers to 25Mb.

```
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.rmem_default=26214400
sudo sysctl -w net.core.wmem_max=26214400 
sudo sysctl -w net.core.wmem_default=26214400
```

Set MTU on all to the OSDD connected interfaces to jumboframes. No impact on UDPCAST due to fixed maximum packetsize but will be useful for other applications. 

```ifconfig <<enp0s3>> mtu 9000```

## Packet loss (almost) explained
[Packet loss explained](packetloss_explained.md)
