# Get started with Data Diodes

This Github is created to share knowledge about data diodes to a wider audience. Since the data diode concept of unidirectional traffic is easy to understand we noticed that when starting with the data diodes in the real world there are some barriers to overcome.

First is getting your hands on data diode hardware, this we solved in the [hardware](datadiode_hardware_setups.md) section.

Second is understanding how data is transfered through a data diode because unidirectional network traffic has some issues which can result in packet loss. This is described in [Packet loss explained](packetloss_explained.md). We think this is one of the main issues you need to understand and overcome before implementing data diodes in production.

Last part is getting some first successes when experimenting the data diode technology. It's a good thing to have a working setup before developing more complex implementations. For this we created the [workshop](workshop/readme.md) based on open source tools to explain you step by step how to send a message, a large (>1Gb+) batch file and an audio/video stream using the data diode.

By the end of the workshop you should be able to proceed with your own projects or research.

## Workshop working with data diodes
[Click here for the workshop](workshop/readme.md)

## Packet loss (almost) explained
[Packet loss explained](packetloss_explained.md)

## Example data-diode hardware setups
[Datadiode hardware setups](datadiode_hardware_setups.md) <br>
Extra: [€25 euro functional data-diode demonstrator](https://github.com/Vrolijk/OSDD/blob/main/examples/25_euro_data-diode_demonstator.md) Try could/should this before buying a real data diode.

## Various links 
[Various links to related content](external_content.md)

## Help needed to improve this project
[Linux kernel packet loss - Help needed!](https://github.com/Vrolijk/OSDD/issues/6)
