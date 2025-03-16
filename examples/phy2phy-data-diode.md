Below is a manual designed by Grok AI for a student to build a cheap 1Gb unidirectional network device based on the PCB design we’ve developed. It includes step-by-step instructions, research questions, and alternatives where applicable to encourage learning and experimentation. The manual assumes basic electronics knowledge (e.g., soldering, reading schematics) but keeps explanations clear for a student audience.

---

# Student Manual: Building a Cheap 1Gb Unidirectional Network Device

## Overview
This project guides you through building a simple, low-cost network device that takes Gigabit Ethernet traffic from one RJ45 port (Receiver) and forwards it unidirectionally to another RJ45 port (Sender). It’s powered by USB-C and includes LEDs to show link status and data activity. You’ll learn about Ethernet PHY chips, PCB assembly, and basic circuit design while keeping costs low.

### Learning Goals
- Understand how Ethernet PHY chips work.
- Assemble a functional PCB with minimal components.
- Explore trade-offs in cost, size, and complexity.

### Tools and Skills Needed
- Soldering iron and solder
- Multimeter (for troubleshooting)
- Basic PCB design software (e.g., KiCad, optional)
- Wire cutters/strippers
- Patience and curiosity!

---

## Bill of Materials (BOM)
| **Component**             | **Quantity** | **Description**                     | **Approx. Cost** | **Notes**                     |
|---------------------------|--------------|-------------------------------------|------------------|-------------------------------|
| Ethernet PHY Chip         | 2            | Realtek RTL8211 or similar          | $1-2 each        | Gigabit-capable PHY          |
| RJ45 Connector            | 2            | Unshielded, with magnetics          | $0.50-1 each     | For receiver and sender      |
| USB-C Connector           | 1            | Power-only (5V input)               | $0.20            | No data pins needed          |
| 3.3V LDO Regulator        | 1            | AMS1117-3.3 or similar              | $0.10            | Converts 5V to 3.3V          |
| 25 MHz Crystal            | 2            | HC-49S package                      | $0.10-0.20 each  | For PHY timing               |
| 22pF Capacitor            | 4            | Ceramic, for crystal loading        | $0.01 each       | 2 per crystal                |
| 0.1µF Capacitor           | 2-4          | Ceramic, for decoupling            | $0.01 each       | Near PHY power pins          |
| LED                       | 4            | 2 for link, 2 for activity          | $0.05 each       | Any color (e.g., green/red)  |
| 330Ω Resistor             | 4            | For LED current limiting            | $0.01 each       | Matches LED specs            |
| PCB                       | 1            | Single- or double-sided FR4         | $1-2             | Custom or perfboard          |
| Jumper Wires              | As needed    | For connections (if using perfboard)| Minimal          | Optional                     |

**Total Estimated Cost**: $5-8 (excluding tools and shipping).

---

## Step-by-Step Build Instructions

### Step 1: Understand the Design
The device uses two Ethernet PHY chips:
- **Receiver PHY**: Takes input from the Receiver RJ45 and sends data out its TX pins.
- **Sender PHY**: Receives data on its RX pins and outputs to the Sender RJ45.
- Data flows unidirectionally (Receiver → Sender), with no processing or buffering.
- Power comes from USB-C (5V), stepped down to 3.3V for the PHYs.
- LEDs show if the ports are connected (link) and if data is moving (activity).

**Research Question**: Why do Gigabit Ethernet PHYs need a 25 MHz crystal? Look up the IEEE 802.3 standard for clues!

---

### Step 2: Gather Components
- Source parts from suppliers like DigiKey, Mouser, or AliExpress.
- **Alternative**: Check if your school lab has spare PHY chips or RJ45s. Could you use a different PHY (e.g., Microchip KSZ9031)? What changes would that require?

---

### Step 3: Create or Prototype the PCB
- **Option 1: Perfboard** (Cheaper, Manual):
  - Use a perforated board and solder components directly.
  - Plan your layout: keep PHYs close to RJ45s, and crystals nearby.
- **Option 2: Custom PCB** (Cleaner, Advanced):
  - Download KiCad (free) and draw the schematic (see below).
  - Aim for a single-sided design to save cost, but double-sided is okay if needed.
- **Schematic**:
  - Receiver RJ45 → Receiver PHY (RX pins).
  - Receiver PHY TX pins → Sender PHY RX pins (direct wire connection).
  - Sender PHY TX pins → Sender RJ45.
  - USB-C VBUS → LDO (5V to 3.3V) → PHY VCC pins.
  - Each PHY: 25 MHz crystal + 2x 22pF caps across XTAL1/XTAL2.
  - 0.1µF caps near PHY power pins.
  - LEDs + 330Ω resistors from PHY LINK and ACTIVITY pins to GND.

**Research Question**: Could you share one crystal between both PHYs? What’s the trade-off in cost vs. complexity?

---

### Step 4: Assemble the Circuit
1. **Solder the USB-C Connector**:
   - Connect VBUS (5V) and GND pins only. Ignore data pins (D+, D-).
2. **Add the LDO**:
   - Input: USB-C 5V. Output: 3.3V to PHY VCC pins.
   - Add a 0.1µF cap on input and output for stability.
3. **Place the PHY Chips**:
   - Solder each RTL8211 (or similar) carefully—check pin 1 orientation!
   - Add a 0.1µF cap near each VCC pin.
4. **Connect the Crystals**:
   - For each PHY: Solder a 25 MHz crystal across XTAL1/XTAL2.
   - Add 22pF caps from each crystal pin to GND.
5. **Wire the RJ45s**:
   - Receiver RJ45 → Receiver PHY RX pins (via magnetics).
   - Sender PHY TX pins → Sender RJ45 (via magnetics).
6. **Unidirectional Link**:
   - Connect Receiver PHY TX pins directly to Sender PHY RX pins (e.g., TXD0 to RXD0, TXD1 to RXD1, etc.).
7. **Add LEDs**:
   - Link LED: PHY LINK pin → 330Ω resistor → LED → GND.
   - Activity LED: PHY ACTIVITY pin → 330Ω resistor → LED → GND.
   - Repeat for both PHYs.

**Alternative**: If ACTIVITY pins aren’t available, could you use TX or RX pins for data LEDs? Test it!

---

### Step 5: Test the Device
1. **Power Up**:
   - Plug in a USB-C cable (5V source, like a phone charger).
   - Use a multimeter to check 3.3V at the LDO output.
2. **Check LEDs**:
   - Connect a Gigabit Ethernet source (e.g., a router) to the Receiver RJ45.
   - Connect the Sender RJ45 to a device (e.g., a PC).
   - Link LEDs should light up if connected. Activity LEDs should blink with data.
3. **Test Data Flow**:
   - Send packets (e.g., ping) from the source. Check if they reach the destination.
   - Note: Traffic is one-way only—don’t expect replies through this device!

**Research Question**: Why might the link fail? Hint: Check PHY pin configurations or magnetics wiring.

---

### Step 6: Troubleshoot
- **No Power**: Check USB-C and LDO connections.
- **No Link**: Verify RJ45 wiring and crystal oscillation (use an oscilloscope if available).
- **No Data**: Ensure TX-to-RX connections match (pin-for-pin).

**Alternative**: Add test points (e.g., header pins) to probe signals. Worth the extra cost?

---

## Final Notes
- **Safety**: Don’t exceed 5V input—PHYs can’t handle it!
- **Customization**: Want a smaller size? Try surface-mount parts instead of through-hole.
- **Next Steps**: Research adding a microcontroller to filter packets. How would that change the design?

**Total Build Time**: 2-4 hours (depending on soldering skill).

---

Enjoy building your network device! Let me know if you need help with a specific step or want to explore more alternatives. What do you think you’d improve after building it?