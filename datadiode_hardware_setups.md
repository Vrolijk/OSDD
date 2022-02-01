# Example datadiode hardware setups

## Basic setup

<img src="img_simple_datadiode_setup.png" width=300>

## 2 way uni-directional setup

To be able to send and receive data via seperate interfaces causing a protocol break for most network attacks. This setup also provides control over the received and send data.
In this expample we send an OpenSSL certificate request trough the diode to be signed by the CA. After signing the CA sends the signed certificate trough the second datadiode back to the sender.

<img src="img_2_way_datadiode_setup.png" width=300>

## One proxy to many destionations

Since we are using one way communication it's also possible to use multiple datadiodes and destionations using a switch.

<img src="img_one_to_many_datadiode_setup.png" width=300>

## NTP distribution to multiple stand alone networks

This example shows an example to distribute NTP to multiple networks. Note that this configuration does not support NTPv4 foley's.

<img src="img_NTP_timeserver_to_multiple_networks.png" width=300>

## Garanteed one way span poort to IDS

In this example we prevent the IDS to connect back to the switch via the SPAN port.

<img src="img_span_port_with_diode.png" width=300>

## Virtual datadiode

For testing datadiode applications on one machine its possible to create a Ubuntu VM with 2 interfaces connected to separate local networks.
Using the application daemonlogger you can forward all packets from the first interface to the second.

<img src="img_virtual_datadiode_setup.png" width=300>

**Helpfull links**

***Wavestone-cdt DIY Dyode*** 

DIY Datadiode using 3 copper to fiber converters and a light version using 2 PI zero's and an optocoupler.

Software includes
* Modbus data transfer
* File transfer (DYODE full only)
* Screen sharing (DYODE full only)

https://github.com/wavestone-cdt/dyode 

***Klockcykel Godiode***

DIY Datadiode using 2 modded TPlink copper to fiber converters. Costs +- €65,-

Software includes Go code and Docker. Transferspeed up to 750Mbit.

https://github.com/klockcykel/godiode 

***Open Source Datadiode project ***

Dutch project to build an open source datadiode

https://securitydelta.nl/nl/projects/project/99-open-source-data-diode 
