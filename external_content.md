# Youtube presentations / Webinars

### Webinar CSIAC: Physical Cybersecurity: Using One-Way Data Diodes to Secure Asset Monitoring 1:04:27

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/VSNhiVtTQFA/0.jpg)](https://www.youtube.com/watch?v=VSNhiVtTQFA)

Slides: https://csiac.org/wp-content/uploads/2021/11/CSIAC_Deck_Final_1-2022.pdf 

### ESTCP project overview Data Diodes
https://youtube.com/watch?v=HC3_Dd8KM0E&si=EnSIkaIECMiOmarE <br>
https://www.serdp-estcp.org/projects/details/30717e9d-8325-43fd-a813-6396ae5f7ff6/ew19-5156-project-overview


# Vendors
## Link22
https://link22.eu/products/diode-proxy/

# Projects 
### FLUTE - File Delivery over Unidirectional Transport
Massively scalable multicast distribution solution

The library implements a unidirectional file delivery, without the need of a return channel.
https://github.com/ypo/flute 


## UDPcast as a service

https://github.com/azzid/pmddft

# Examples with proxies

## Basic setup

<img src="img/img_simple_datadiode_setup.png" width=300>

For training you can use a managed switch: [€25 euro data-diode demonstrator](https://github.com/Vrolijk/OSDD/blob/main/examples/25_euro_data-diode_demonstator.md)

## More secure basic setup

In this setup we used 2 TP-Link MC210CS single mode Gigabit mediaconverters, one single mode 50/50 splitter and a fiber filter for additional security.

<img src="img/OSDD_splitter_and_filter.png" width=300>


## 2 way uni-directional setup

To be able to send and receive data via separate interfaces causing a protocol break for most network attacks. This setup also provides control over the received and send data.
In this example we send an OpenSSL certificate request trough the data-diode to be signed by the CA. After signing the CA sends the signed certificate trough the second data-diode back to the sender.

<img src="img/img_2_way_datadiode_setup.png" width=300>

## One proxy to many destinations

Since we are using one way communication it's also possible to use multiple data-diodes and destinations using a switch.

<img src="img/img_one_to_many_datadiode_setup.png" width=300>

## NTP distribution to multiple stand alone networks

This example shows an example to distribute NTP to multiple networks. Note that this configuration does not support NTPv4 foley's.

<img src="img/img_NTP_timeserver_to_multiple_networks.png" width=300>

## Guaranteed one way span port to IDS

In this example we prevent the IDS to connect back to the switch via the SPAN port.

<img src="img/img_span_port_with_diode.png" width=300>

## Virtual data-diode

For testing data-diode applications on one machine its possible to create a Ubuntu VM with 2 interfaces connected to separate local networks.
Using the application daemonlogger you can forward all packets from the first interface to the second.

<img src="img/img_virtual_datadiode_setup.png" width=300>

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

### Mitcdh 

Example how to configure a Cisco switch as a data-diode

https://github.com/mitcdh/diode-switch-config 

### svenseeberg

Example using Raspberry PI's

https://github.com/svenseeberg/data-diode


## Dutch Open Source Datadiode project

Dutch project to build an open source datadiode

https://securitydelta.nl/nl/projects/project/99-open-source-data-diode 

### Georgesrusu

Webportal in combination with BlindFTP (not tested). Read the (good) report first.

https://github.com/georgesrusu/managementSecuDataDiode/blob/master/Rapport/rapport.pdf 

### Cylab-be

Good resource for documentation and webbased solution.

https://gitlab.cylab.be/cylab/data-diode

### MeghaSharma31

Nice report on data-diodes using the ATM protocol.

https://github.com/MeghaSharma31

### Cea-sec Hairgap

Hairgap is a set of tools to transfer data over a unidirectional network link. (Aplha)

https://github.com/cea-sec/hairgap

### Bhanq

The goal of this project was to implement a (virtual) Data Diode according to some CyberSecurity frameworks NIST SP 800-30 : Risk analysis report and Common criteria.

https://github.com/BHanq/DataDiode

### TFC

https://github.com/maqp/tfc/wiki/TTL-Data-Diode-(PCB) <br>
https://www.kitploit.com/2020/03/tinfoil-chat-onion-routed-endpoint.html 

