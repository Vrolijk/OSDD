# Example data-diode hardware setups

## Physical data-diode setup

In this setup we used 3 TP-Link ~~MC200CM multi mode~~ MC210CS single mode Gigabit mediaconverters and a PLC Fibre Splitter 1X4 SC/UPC-interface. Please note that the splitter is single mode, not multi mode!

The TX-mediaconverter TX-port is connected with the IN-fiber from the splitter and the 4th splitted fiber to the RX-port to simulate a link.<br>
The RX3 mediaconverter RX-port is connected with the 3th splitter fiber. <br>
The RX2 mediaconverter RX-port is connected with the 2th splitter fiber. <br>
The 1th fiber is not connected but could also be connected to a  mediaconverter but i only had three converters available.

This way we created a one to many datadiode setup but this could also be done with a 1x2 PLC splitter with only 2 mediaconverters. <br> See 2nd simplyfied image.

<img src="img/TP-Link-1to4-datadiode.jpg" width=300> <img src="img/TP-Link-1to4-datadiode-simple.jpg" width=300>


# Lessons learned

Understand the difference between multi mode and single mode fiber. 
We noticed network errors on the TX proxy. The cause was a single mode fiber splitter in combination with multi mode mediaconverters.
TCPDUMP output:

```
20:10:26.441796 MPCP, Opcode Pause, length 46
20:10:26.442321 MPCP, Opcode Pause, length 46
20:10:26.442845 MPCP, Opcode Pause, length 46
...... and many more..... 
```

So depending on your cables you can use the MC200CM multi mode or MC210CS single mode media converters. 
