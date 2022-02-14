# Example data-diode hardware setups

## Basic setup

<img src="img_simple_datadiode_setup.png" width=300>

## 2 way uni-directional setup

To be able to send and receive data via separate interfaces causing a protocol break for most network attacks. This setup also provides control over the received and send data.
In this example we send an OpenSSL certificate request trough the data-diode to be signed by the CA. After signing the CA sends the signed certificate trough the second data-diode back to the sender.

<img src="img_2_way_datadiode_setup.png" width=300>

## One proxy to many destinations

Since we are using one way communication it's also possible to use multiple data-diodes and destinations using a switch.

<img src="img_one_to_many_datadiode_setup.png" width=300>

## NTP distribution to multiple stand alone networks

This example shows an example to distribute NTP to multiple networks. Note that this configuration does not support NTPv4 foley's.

<img src="img_NTP_timeserver_to_multiple_networks.png" width=300>

## Guaranteed one way span port to IDS

In this example we prevent the IDS to connect back to the switch via the SPAN port.

<img src="img_span_port_with_diode.png" width=300>

## Virtual data-diode

For testing data-diode applications on one machine its possible to create a Ubuntu VM with 2 interfaces connected to separate local networks.
Using the application daemonlogger you can forward all packets from the first interface to the second.

<img src="img_virtual_datadiode_setup.png" width=300>

# Helpful links

## Wavestone-cdt DIY Dyode

DIY Datadiode using 3 copper to fiber converters and a light version using 2 PI zero's and an optocoupler.

Software includes
* Modbus data transfer
* File transfer (DYODE full only)
* Screen sharing (DYODE full only)

https://github.com/wavestone-cdt/dyode 

## EBUJOLD data-diode

DIY data-diode like the Wavestone solution. Good explanation about the configuration of the media converters in the wiki under hardware.

https://github.com/EBUJOLD/data-diode 

## Klockcykel Godiode

DIY Data-diode using 2 modded TP-link copper to fiber converters. Costs +- €65,-

Software includes Go code and Docker. Transfer speed up to 750Mbit.

Please note: Soldering requires a microscope due to the size of the pcb 

https://github.com/klockcykel/godiode 

## Dutch Open Source Datadiode project

Dutch project to build an open source datadiode

https://securitydelta.nl/nl/projects/project/99-open-source-data-diode 
