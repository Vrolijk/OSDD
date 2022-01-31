# Packet loss (almost) explained

:exclamation: *I like telling UDP jokes because I **do** care if you don't get them.*

On of the main issues when using datadiodes is not being able to check if the UDP packets you send arrived at the receiving proxy. During testing using large files we found out that one of the main issues is that the receiving application is not able to read the UDP packets quick enough from the rx_queue.
In this overview we try to explain this. 

Please comment on this article if you can help because we still havent found a final solution for this problem.

![Overview packet loss](/datadiode_packetloss.png)

In this overview we use 5 steps to explain the issue:

1. Sender application sends/receive the data
2. The application sends the data to the TX_QUEUE in kernel space
3. The UDP packets are transfed over the cable trough the datadiode to the receiver
4. The receiver receives the UDP packets and places them in the RX_QUEUE
5. The receiver application **reads** the UDP packets from the RX_QUEUE, processes them and writes the packets to the datafile

We found out that most of the packet loss happens on the receiving machine when the application is not able to read the RX_QUEUE fast enough. When the RX_QUEUE is full the kernel drops the packets and data is lost.

Possible solutions

1. Send the data slower from the sender. The applications UDPcast or PV (pipe viewer) are able to send the data on a lower speed.
2. Enlarge the RX_QUEUE using sysctl. This only helps for small bursts, when sending multiple Gb's this has no use.
3. Use FEC (Forward Error Control). The application UDPcast has the option to add FEC.
4. Faster processing at the receiving application. Try to reduce the CPU load of the receiving application and/or limit other applications using the CPU
5. Faster writing to disk. Use SSD or memdisk to write the data.

## Monitoring packetloss

Monitor UDP queues and packets dropped

```cat /proc/net/udp```

or use netstat

```to do add netstat command | grep IP:PORT```

**TO DO**

By monitoring the UDP RX_QUEUE during a fast and large file transfer we can see the queue filling up and after a few seconds followed by packets dropped.

We did not try to monitor the softnet_stat to find out the root cause of the rx_queue filling up.

```cat /proc/net/softnet_stat```

**Helpfull links**

https://arthurchiao.github.io/blog/monitoring-network-stack/ 

https://github.com/wavestone-cdt/dyode 

https://securitydelta.nl/nl/projects/project/99-open-source-data-diode 


