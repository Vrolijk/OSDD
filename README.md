# Send single large file and multiple files datadiode test using UDPcast: 

In this article we will show how to send one or multiple files trough a datadiode using UDPCAST.

For this example we use 2 proxies with a gigabit datadiode in the middle. 

## Single file

*all items between <<variable>> are variables and can be found in the application man pages.*

**Create random file of 5Gb**

```head -c 5120M /dev/urandom > 5gb-testfile.tmp```

## Multiple files

**Transfer using udpcast trough datadiode with different parameters**

Sender: 

```udp-sender --interface <<enp0s8>> --async --fec <<8x8/128>> --max-bitrate <<600Mbps>> --file 5gb-testfile.tmp –broadcast```

Receiver: 

```udp-receiver –nosync –interface <<enp0s3>> --file 5gb-testfile.tmp```

**validate received file using sha256sum**

On both proxies the outcome should be identical: 

```sha256sum 1gb-testfile.tmp```

**Possibilities for tweaking:**

UDP buffers to 25Mb.

```
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.rmem_default=26214400
sudo sysctl -w net.core.wmem_max=26214400 
sudo sysctl -w net.core.wmem_default=26214400
```

Set MTU on all to the OSDD connected interfaces to jumboframes. No impact on UDPCAST due to fixed maximum packetsize but will be useful for other applications. 

```ifconfig <<enp0s3>> mtu 9000```




**Example multiple files/directory**

Sending large and multiple files trough a datadiode / unidirectional network connection using udpcast and tar

Receiver:

```udp-receiver --nosync --interface enp0s3 | tar –x```

Sender: 

```tar -c /data/ | udp-sender --interface enp0s8 --async --fec 8x8/64 --max-bitrate 800Mbps --broadcast --autostart 1 --nokbd ```
