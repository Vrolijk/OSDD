# Workshop level 2

After finnishing the easy part of the workshop you should understand the basics. From here you could start some more use cases. If you can solve or help with one or more of the use cases please leave a comment under discussions.

# Use Case XDP / Packetloss
We still have a problem with packetloss because of the way the Linux networkstack handles UDP packets. In this use case we challenge you to configure the sender and receiver (Ping and Pong) to bypass the network stack by using UDP.
Goal is to send data from 10.0.0.1 to 10.0.0.2 without packetloss.
Some nice sources to start:<br>
https://github.com/xdp-project/xdp-tutorial <br>
https://www.tigera.io/learn/guides/ebpf/ebpf-xdp/ <br>

# Use Case Streaming media server (Mistserver)
In the workshop you played a little with a single mediastream from VLC to VLC. Can you expand this to a more advanced setup using https://mistserver.org/ <br>  
