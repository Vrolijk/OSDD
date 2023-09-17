# Getting started with Data Diodes

<img align="right" width="200" src="img/street_sign_one_way-source_wallpaperflare.jpg">
This Github is created to share knowledge about data diodes to a wider audience. The data diode concept of unidirectional traffic is easy to understand but we noticed that when starting with the data diodes in the real world there are some barriers to overcome. This workshop will help you to start with the basic concept of data diodes while keeping the costs to a minimum<br><br> 


First issue is getting your hands on data diode hardware, which we solved in the [hardware](datadiode_hardware_setups.md) section.


Second issue is understanding how data is transferred through a data diode because unidirectional network traffic has some issues which can result in packet loss. This is described in [Packet loss explained](packetloss_explained.md). We think this is one of the main issues you need to understand and overcome before implementing data diodes in production.

Last issue is getting your first successes when experimenting with data diodes in combination with software. It's a best practice to have a working setup before developing more complex implementations. For this we created the [workshop](workshop/readme.md) based on open source tools to explain you step by step how to: <br> 
1) send a single message, <br>
2) transfer a large (>1Gb+) batch file (stop using external drives) and <br>
3) stream audio/video from the internet to an offline machine using the data diode.

By the end of the workshop you should be able to understand how to use data diodes in your own projects or research.

## Workshop working with data diodes
[Click here for the workshop](workshop/readme.md)

## Packet loss (almost) explained
[Packet loss explained](packetloss_explained.md)

## Example data-diode hardware setups
[Datadiode hardware setups](datadiode_hardware_setups.md) <br>
Note: Try this demonstrator in combination with the workshop before buying or building a real data diode. [€25 euro functional data-diode demonstrator](https://github.com/Vrolijk/OSDD/blob/main/examples/25_euro_data-diode_demonstator.md) 

## Various links 
[Various links to related content](external_content.md)

## Help needed to improve this project
[Linux kernel packet loss - Help needed!](https://github.com/Vrolijk/OSDD/issues/6)
