# Workshop level 2

<img align="right" width="200" src="../img/bb_round_2.jpg">
After finishing the easy part of the workshop you should understand the basics. From here you could start some more use cases. If you can solve or help with one or more of the more advanced use cases please share your results under [discussions](https://github.com/Vrolijk/OSDD/discussions/7) . 


## Use Case Add the FLUTE protocol for file/batch transfer
On https://github.com/ypo/flute there is an example for filetransfer using the FLUTE protocol. Are you able to implement this in your setup? 

## Use Case Streaming media server (Mistserver)
In the workshop you played a little with a single mediastream from VLC to VLC. Can you expand this to a more advanced setup using https://mistserver.org/   
<br><i>Tip: stream a .mp4 and forward it using tsudp.</i> 

## Use Case File transfer on Windows using Powershell
Sans published a wonderful document "Tactical Data Diodes in Industrial Automation and Control Systems". On page 23 there is a PowerShell TFTP example for batch file transfer. Are you able to reproduce and/or improve this? 
https://www.sans.org/white-papers/36057/ 

## Use Case reproduce the DYDOE setup
On https://github.com/wavestone-cdt/dyode/tree/master/DYODE%20v1%20(full) there are three use cases created in Python. Are you able to reproduce and/or improve them? 
- File transfer
- Modbus data transfer
- Screen sharing

## Use Case file transfer using Go
On https://github.com/klockcykel/godiode is a nice example to transfer files using Go. This project also supports Jumbo Frames. 

## Read the following documents

### SANS: Tactical Data Diodes in Industrial Automation and Control Systems
https://www.sans.org/white-papers/36057/

### OWL: All Data Diodes Are Not Equal
https://scadahacker.com/library/Documents/White_Papers/Owl%20-%20All%20Data%20Diodes%20Are%20Not%20Equal.pdf 

### FEND: Low-Cost, Plug-and-Play Data Diodes for Protection and Monitoring of DoD Facility Equipment 
https://apps.dtic.mil/sti/pdfs/AD1187369.pdf

## Use Case XDP to prevent Packetloss
We still have a problem with packetloss because of the way the Linux networkstack handles UDP packets. In this use case we challenge you to configure the sender and receiver (Ping and Pong) to bypass the network stack by using UDP.
Goal is to send data from 10.0.0.1 to 10.0.0.2 without packetloss. We didn't test this but would like to know if this solves the packetloss problem. Please share your findings, config and results.
Some nice sources to start:<br>
https://github.com/xdp-project/xdp-tutorial <br>
https://www.tigera.io/learn/guides/ebpf/ebpf-xdp/ <br>


For more external sources see: https://github.com/Vrolijk/OSDD/blob/main/external_content.md
