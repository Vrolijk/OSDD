# Packet loss (almost) explained

:exclamation: *I like telling UDP jokes because I **do** care if you don't get them.*

One of the main issues when using data diodes is not being able to check if the UDP packets you send arrived at the receiving proxy. During testing using large files we found out that one of the main issues is that the receiving application is not able to read the UDP packets quick enough from the rx_queue.
In this overview we try to explain this. 

*Please add an issue for this article if you can help because we still haven't found a final solution for this problem.*

![Overview packet loss](img/datadiode_packetloss.png)

In this overview we use 5 steps to explain the issue:

1. Sender application sends/receive the data
2. The application sends the data to the TX_QUEUE in kernel space
3. The UDP packets are send over the cable trough the data diode to the receiver
4. The receiver receives the UDP packets and places them in the RX_QUEUE
5. The receiver application **reads** the UDP packets from the RX_QUEUE, processes them and writes the packets to the file

We found out that most of the packet loss happens on the receiving machine when the application is not able to read the RX_QUEUE fast enough. When the RX_QUEUE is full the kernel drops the packets and data is lost.

## Possible solutions

1. Send the data slower from the sender. The applications UDPcast or PV (pipe viewer) are able to send the data on a lower speed.
2. Enlarge the RX_QUEUE using sysctl. This only helps for small bursts, when sending multiple Gb's this has no use.
3. Use FEC (Forward Error Control). The application UDPcast has the option to add FEC.
4. Faster processing at the receiving application. Try to reduce the CPU load of the receiving application and/or limit other applications using the CPU
5. Faster writing to disk. Use SSD or memdisk to write the data.

## Monitoring packet loss

Monitor UDP queues and packets dropped. We are still looking into the best way to monitor the queues and this can be done on several ways.<br>
Monitor both the sender and receiver. 

```cat /proc/net/udp```

or use netstat

**sender** <br>
```sudo netstat -c -udp -an | grep "9001"``` <br>
[recording](https://raw.githubusercontent.com/Vrolijk/OSDD/main/img/OSDD-send-512Mb.mp4) 

**receiver** <br> 
```sudo netstat -c -udp -an | grep ".255:9000"``` <br>
[recording](https://raw.githubusercontent.com/Vrolijk/OSDD/main/img/OSDD-receive-512Mb.mp4)


or use ss

```watch -n 1 "ss -u -a -p -t '( sport = :9000 )'"```

or use traffic control (tc). 

```tc -s qdisc show dev eth0```

Bottom line, we noticed that the Recv-Q fills and the UDP-receiver application stops/crashed. 
Recv-Q is the count of bytes not copied by the user program connected to this socket.

Except for increasing the sysctl net.core.rmem_max we are still looking for a solution how to prevent the Recv-Q dropping packets. Please comment if you can help.

```sudo sysctl -w net.core.rmem_max=32777216```

Monitoring the softnet_stat we saw no increase of queues.

```cat /proc/net/softnet_stat```

### Monitoring using Dropwatch
https://www.cyberciti.biz/faq/linux-show-dropped-packets-per-interface-command/

```
sudo apt-get install libpcap-dev libnl-3-dev libnl-genl-3-dev binutils-dev libreadline6-dev autoconf libtool pkg-config build-essential```

git clone https://github.com/nhorman/dropwatch
cd dropwatch
./autogen.sh
./configure
make
sudo make install
```
<b> check the current settings</b>
```
cat /proc/sys/kernel/kptr_restrict
sudo su
echo 0 > /proc/sys/kernel/kptr_restrict

dropwatch -l list

sudo dropwatch -l kas

start
```
# Tip 1: tc qdisc adjustment

```
sudo gedit /etc/systemd/system/optimize-fq_codel.service
```

```
[Unit]
Description=Optimize and Limit fq_codel qdisc for Gigabit Data Diode
After=network.target

[Service]
Type=oneshot
ExecStartPre=/sbin/ip link set enp1s0 txqueuelen 10000
ExecStartPre=/sbin/ip link set enp1s0 mtu 9000
# Remove any existing qdisc before adding new one
ExecStartPre=/sbin/tc qdisc del dev enp1s0 root
ExecStart=/sbin/tc qdisc add dev enp1s0 root handle 1: htb default 10
ExecStart=/sbin/tc class add dev enp1s0 parent 1: classid 1:1 htb rate 990Mbit ceil 990Mbit
ExecStart=/sbin/tc class add dev enp1s0 parent 1:1 classid 1:10 htb rate 990Mbit ceil 990Mbit
ExecStart=/sbin/tc qdisc add dev enp1s0 parent 1:10 handle 10: fq_codel limit 20000 flows 4096 quantum 9000 memory_limit 64M target 1ms interval 10ms noecn
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl enable optimize-fq_codel.service
sudo systemctl start optimize-fq_codel.service
```
Note: Also modify the sysctl queues, not doing this caused packet loss.

```
sudo gedit /etc/sysctl.conf
```
Append a config directive as follow at the end of the file, save and close the document:

```
net.core.rmem_max = 32777216
net.core.rmem_default = 32777216
net.core.wmem_max = 32777216 
net.core.wmem_default = 32777216
net.core.netdev_max_backlog = 100000
net.ipv4.udp_mem="12148128 16197504 67108864"
```
Activate sysctl changes:
```
sudo sysctl -p /etc/sysctl.conf 
```

# To do 1

CPU - NIC Isolation: https://github.com/Vrolijk/OSDD/issues/10 First step in exploration.. 

# To do 2

Good story about tuning TCP. Perhaps lowering the garbage collection could help to reduce packet loss on the receiving side.

https://blog.cloudflare.com/the-story-of-one-latency-spike/ 

https://unix.stackexchange.com/questions/611981/udp-packet-drops

**Helpful links**

https://arthurchiao.github.io/blog/monitoring-network-stack/ 

https://www.sobyte.net/post/2022-05/linux-udp-packet-drop-debug/

https://iopscience.iop.org/article/10.1088/1748-0221/15/09/T09005/pdf <br>
  B System configuration<br>
  The following commands were used (performed as superuser) to change the system parameters on CentOS. The examples below modifies network interface eno49. This should be changed to match the name of the interface on the actual system. <br>
> sysctl -w net.core.rmem_max=12582912 <br>
> sysctl -w net.core.wmem_max=12582912 <br>
> sysctl -w net.core.netdev_max_backlog=5000 <br>
> ifconfig eno49 mtu 9000 txqueuelen 10000 up <br>

More details about UDP tuning: <br>
https://gilbertasm.github.io/2018/09/13/tunning-udp-buffers.html <br>
https://blog.packagecloud.io/monitoring-tuning-linux-networking-stack-sending-data/#monitoring-udp-protocol-layer-statistics
