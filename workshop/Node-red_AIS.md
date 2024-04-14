Pending : raw instructions

Install node-red : https://nodered.org/docs/getting-started/local <br>
Register at https://aisstream.io/ using your Github account <br>
Follow the instruction on: https://www.youtube.com/watch?v=h9OQuxB_aGs <br>

Once you receive the AIS events send them from PING to PONG using UDP-out on 10.0.0.2 port 9999

On Pong use UDP-in listening on 9999

## To prevent packetloss check the UDP buffer
Still in development, help is welcome!

First we need to measure the UDP buffer using the TC command. To excecute this command from Node-red we use the excec function. Create a flow like below. In this example we add the debug function with count to show the effect.
<img width="400" src="/img/node-red_flow_1.png"><br>

Edit the excec node<br>
<img width="400" src="/img/node-red_flow_2.png"><br>

Use the command: <br>
``` tc -s qdisc show dev enp1s0 | awk -F 'backlog ' '{print $2}' | awk -F 'b' '{print $1}' | awk 'NF'``` 
<br><i> I'm open for a more efficient way </i>:) <br><br>
Edit the switch node<br>
<img width="400" src="/img/node-red_flow_3.png"><br>

Use the following filter: (note the number variable)<br><br>

Since i'm new to Node-red i'm still looking for a way to wait untill the UDP queue is 0 before sending the event to the UDP-out node. 

