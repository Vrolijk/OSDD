# Open items and ideas, help appreciated to test and improve ##

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
``` watch -n 1 "ss -u -a -p" ``` 



## Force network queue to drop packets: Netcat pipe large file
On PONG start: <br>
```nc -l -u -w 1 -p 9999 > 1gb-testfile.tmp```

Then start on PING: <br>
```cat 1gb-testfile.tmp | nc -w 1 -u 10.0.0.2 9999```


Probably this went wrong. Try to reduce the speed with PipeViewer PV to find an optimal speed for your configuration.<br>
On PONG start: <br>
```nc -l -u -w 1 -p 9999 > 1gb-testfile.tmp```

Then start on PING: <br>
```sudo apt install pv```
<br>
```cat 1gb-testfile.tmp | pv -L 30m | nc -w 1 -u 10.0.0.2 9999```
<br><br><br><br>

# Data diode basics and problems
The data diode isn't the solution for all your problems. Here is an overview of the various ways to bridge 2 networks. <br><i>Note: This overview misses the Cross Domain Solutions (CDS). </i><br>

<img src="/img/datadiode_position_security_landscape.png" width="600"> <br>


This is a high level overview of the network connection layers. The data diode will only allow data from A to B. This will break a lot protocols on all OSI layers because handshakes and validations will not work. Example: The TCP protocol first checks the connection by sending a SYN packet, the receiving computer will receive the packet but the diode stops the ACK reply. Since UDP is stateless, no handshake needed, we will use this protocol in most use-cases.

<img src="/img/TCP-IP-model-vs-OSI-model.png" width="300"> <br>


If we want to prevent data leakage from the TX proxy to the RX proxy need to add filters and policies on the sending and/or receiving proxies. The data diode just forwards all packets and doesn't care about the content of the packets.<br> 
This makes the data diode not only a network solution but we need some extra work to add protection on all OSI layers including the user and content (OSI layer 8 and 9?) by including filtering and processes.<br>
<img src="/img/img_simple_datadiode_setup.png" width="300"> <br>



Futher reading about udp and network tuning:  https://blog.cloudflare.com/how-to-receive-a-million-packets/ 

[^2]: https://alibaba-cloud.medium.com/analysis-of-udp-packet-loss-problem-in-linux-system-a5b6bd59d97b

# socat
socat can send packets via various protocols and as raw packets. Need to test the options. 


