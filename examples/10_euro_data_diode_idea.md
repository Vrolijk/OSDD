# Turning a €10 switch into a data diode - affordable cybersecurity for OT environments

In the world of cybersecurity, **data diodes** are often seen as the bank vaults of secure data transfer—impenetrable, expensive, and complex. But what if you could achieve robust, 
unidirectional data flow for just €10 using a common network switch? By tweaking the EEPROM registers of an unmanaged switch with an RTL8367S chip, we can create a low-cost data diode perfect for operational technology (OT) 
environments and micro segmentation. Sometimes, all you need is a good lock, not a vault.

## The approach
The RTL8367S, a chip found in many affordable unmanaged switches (and even cheaper than some managed ones), handles Ethernet switching with remarkable flexibility. 
By accessing and modifying the switch’s EEPROM registers, you can reprogram its behavior to enforce **unidirectional data flow**—the hallmark of a data diode. 
This means data can move from a source (e.g., an OT sensor) to a destination (e.g., a monitoring system) without any possibility of reverse communication, all for the price of a coffee.

## Redefining the data diode mindset
The biggest barrier to adopting data diodes is the misconception that they must be fortress-like solutions, reserved for high-security environments like defense or finance.
In reality, many OT use cases don’t need a bank vault—they need a **reliable lock**.
A €10 data diode provides just that: a simple, effective way to ensure data flows one way, reducing attack surfaces without unnecessary complexity.

## How can we do it?
1. **Identify the Switch**: Choose an unmanaged switch with the RTL8367S chip, often found in budget models costing around €10 - for example, the **TP-Link LS1005G**
2. **Access the EEPROM**: Use tools like an I2C programmer or JTAG interface to read and modify the switch’s EEPROM - for this you can use a CH341A USB programmer
3. **Reconfigure Registers**: Adjust the switch’s port settings to disable reverse traffic, effectively creating a one-way data path. For example, you can set specific ports to forward packets in one direction while dropping all incoming traffic from the destination.
4. **Test and Deploy**: Verify the unidirectional flow with packet capture tools and deploy the switch in your OT network.

## Why this matters for OT and micro segmentation
In OT environments—like manufacturing plants, energy grids, or water treatment facilities—security is critical, but budgets are often tight. Traditional data diodes, costing thousands of euros, are overkill for many use cases. A €10 data diode offers:
- **Microsegmentation**: Isolate OT devices to prevent lateral movement by attackers. For instance, sensors can send data to a central system without exposing themselves to external commands.
- **Affordable Security**: Protect critical infrastructure without breaking the bank, making cybersecurity accessible for smaller organizations.
- **Simplicity**: No need for complex configurations or proprietary hardware—just a switch, some register tweaks, and a clear use case.

## Challenges and considerations
While this approach is powerful, it’s not without caveats:
- **Technical Expertise**: Modifying EEPROM registers requires some hardware and networking knowledge, though open-source tools and community guides can help.
- **Limited Features**: Unlike commercial data diodes, this solution prioritizes simplicity over advanced features like protocol conversion or high throughput.
- **Validation**: For critical deployments, rigorous testing is essential to ensure no reverse traffic leaks through misconfigured settings.
- **Undocumented features**: Undocumented and vendor specific features are a major security risk in this setup.

# The experiment

For this we bought a €9,99 TP-Link LS1005G 5 port switch, removed the eeprom and placed it on an external print and made a connector on the switch.
You can also flash the EEPROM chip in place if your USB programmer comes with a suitable clip.
Via the CH341 USB we connected the eeprom to a PC to read the firmware/register. 
In [AsProgrammer](https://github.com/therealdreg/asprogrammer-dregmod) we used the setting IC-> I2C -> 24cxxx -> _24C02.

<br><img src="../img/LS1005G-eeprom-mod.JPG" width="600"> <br>

**Full register including blanks (FF)** <br>
```
00000000: 56 80 16 1D 69 0A 01 1D  E0 03 1B 20 9A 80 1C 20
00000010: 11 89 1B 20 A3 80 1C 20  33 92 1B 20 AC 80 1C 20
00000020: 44 A4 1B 20 9F 80 1C 20  20 6B 1B 20 A8 80 1C 20
00000030: 22 6B 1B 20 B1 80 1C 20  23 6B 01 1D 1F 00 18 00
00000040: 00 00 38 00 00 00 58 00  00 00 78 00 00 00 98 00
00000050: 00 00 41 1D 00 00 FF FF  FF FF FF FF FF FF FF FF
00000060: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
00000070: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
00000080: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
00000090: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
000000A0: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
000000B0: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
000000C0: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
000000D0: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
000000E0: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
000000F0: FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
```
 <br>
**Register breakdown:** <br>
56 80                    *Read eeprom until position 0x00000056 (see first FF), change to 13 C2 00 00 to brick the switch... * <br>
16 1D 69 0A 01 1D E0 03  *Unknown* <br>
 <br>
1B 20 9A 80 1C 20 11 89  *Pattern 1B 20 ?? 80 1C 20 ?? ?? (6 times)*  <br>
1B 20 A3 80 1C 20 33 92  <br>
1B 20 AC 80 1C 20 44 A4  <br>
1B 20 9F 80 1C 20 20 6B  <br>
1B 20 A8 80 1C 20 22 6B  <br>
1B 20 B1 80 1C 20 23 6B  <br>
 <br>
01 1D 1F 00 *Unknown* <br>
18 00 00 00 *Pattern 18, 38, 58, 78, 98* <br>
38 00 00 00  <br>
58 00 00 00  <br>
78 00 00 00  <br>
98 00 00 00  <br>
41 1D 00 00 FF FF FF FF <br>
 <br>

## How to interpret the hex dump

The register works in pairs. So the first pair [56 80 16 1D] set how far the into EEPROM should be read.
You can read the pair as an instruction to SET value [56 80] TO [16 1D] 

You can translate [56 80] to hex '0x5680'.  Decode the Value `0x5680` 

Hex `0x5680` in binary is:

```
0x5680 = 0101 0110 1000 0000 (binary)
          |||| |||| |||| ||||
          |||| |||| |||| |||└─ Bit 0
          |||| |||| |||| ||└── Bit 1
          |||| |||| |||| |└─── Bit 2
          |||| |||| |||| └──── Bit 3
          |||| |||| |||└────── Bit 4
          |||| |||| ||└─────── Bit 5
          |||| |||| |└──────── Bit 6
          |||| |||| └───────── Bit 7
          |||| |||└─────────── Bit 8
          |||| ||└──────────── Bit 9
          |||| |└───────────── Bit 10
          |||| └────────────── Bit 11
          |||└─────────────── Bit 12
          ||└──────────────── Bit 13
          |└───────────────── Bit 14
          └────────────────── Bit 15
```

So:

```
Bit 15 = 0
Bit 14 = 1
Bit 13 = 0
Bit 12 = 1
Bit 11 = 0
Bit 10 = 1
Bit 9  = 1
Bit 8  = 0
Bit 7  = 1
Bit 6  = 0
Bit 5  = 0
Bit 4  = 0
Bit 3  = 0
Bit 2  = 0
Bit 1  = 0
Bit 0  = 0
```

## How to find specific registers

We can find specific functions in the programming guide found [here](https://github.com/shiroichiheisen/Realtek-Unmanaged-Switch-Arduino-Library/blob/main/programming%20guide/Realtek_Unmanaged_Switch_API_Document.pdf).
Once we have found the specific setting we are looking to modify, lets say port isolation for example we need to find the function relating to port isolation, in this case the function is `rtk_port_isolation_set`.
This programming guide will also point us at the C function that implements the feature, in this case it's [rtl8367c_asicdrv_portIsolation.c](https://github.com/shiroichiheisen/Realtek-Unmanaged-Switch-Arduino-Library/blob/ccd863d61a90e90f096fbc77e3959eadce914213/rtl8367c_asicdrv_portIsolation.c#L4).
By following the logic from the implementation function we can ultimately find the register we need to modify, these mostly live in [rtl8367c_reg.h](https://github.com/shiroichiheisen/Realtek-Unmanaged-Switch-Arduino-Library/blob/main/rtl8367c_reg.h).

```c
#define RTL8367C_REG_PORT_ISOLATION_PORT0_MASK 0x08a2
```

In this instance the port isolation mask address for port 1 is `0x08a2`

## How to set the values of specific registers

As mentioned [previously](#how-to-interpret-the-hex-dump) the registers are in pairs, such that to configure a specific value in a specific register we need to do:

```
05 13 00 C0 -> means load 0xC000 to register 0x1305
```

So to enable port isolation on port 1 for all other ports we would need to add:

```
a2 08 00 00 -> means load 0x0000 to register 0x08a2
```

Remember we need to tell the EEPROM to initial read this far, so we have to tell the first two bytes to read 4 bytes further into EEPROM.

# Resources

If you have any issues setting anything up feel free to reach out directly by dropping a note in discussions here: https://github.com/lhalf/OSDD/discussions

Good resource: https://github.com/tomazas/RTL8XXX-Switch. Added port mirroring to the TP-Link SG105 and SG108 including firmware samples.
RTL8367S datasheet https://www.framboise314.fr/wp-content/uploads/2021/06/RTL8367S-CG_Datasheet.pdf
RTL8367 programming guide https://cdn.jsdelivr.net/gh/libc0607/Realtek_switch_hacking@files/Realtek_Unmanaged_Switch_ProgrammingGuide.pdf
Realtek_Unmanaged_Switch_API_driver https://github.com/shiroichiheisen/Realtek-Unmanaged-Switch-Arduino-Library/blob/main/programming%20guide/Realtek_Unmanaged_Switch_ReleaseNote.pdf
Realtek Unmanaged switch API document https://github.com/shiroichiheisen/Realtek-Unmanaged-Switch-Arduino-Library/blob/main/programming%20guide/Realtek_Unmanaged_Switch_API_Document.pdf
Creating the device https://www.lhalf.uk/diode.html

#Cybersecurity #OTSecurity #DataDiode #Microsegmentation #Networking #Innovation