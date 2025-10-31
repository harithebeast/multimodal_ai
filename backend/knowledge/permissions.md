# Quick reference cards — visual cues & compatibility

## Purpose
This document provides quick visual identification guides, compatibility checks, and physical reference points to help users identify components and confirm compatibility before starting hardware upgrades.

---

## RAM identification & compatibility

### Visual identification
- **Desktop RAM (DIMM):**
  - Length: ~133mm (5.25 inches)
  - Pins: 240 (DDR3), 288 (DDR4/DDR5)
  - Notch location: Off-center (prevents backwards insertion)
  - Stands vertically in motherboard slots

- **Laptop RAM (SO-DIMM):**
  - Length: ~67mm (2.6 inches)
  - Pins: 204 (DDR3), 260 (DDR4), 262 (DDR5)
  - Installs at ~30-degree angle, then presses flat
  - Much smaller than desktop RAM

### Compatibility quick check
**Before purchasing, confirm:**
1. RAM type: DDR3 / DDR4 / DDR5 (must match motherboard — NOT interchangeable)
2. Speed: e.g., 2400MHz, 3200MHz (can mix, but will run at slowest speed)
3. Capacity per stick: Check motherboard maximum (e.g., 16GB per slot)
4. Voltage: DDR4 is typically 1.2V, DDR3 is 1.5V
5. Form factor: Desktop uses DIMM, laptops use SO-DIMM

**How to check current RAM:**
- Windows: Press Win+Pause → "Installed RAM" or use CPU-Z (free tool)
- macOS: Apple logo → About This Mac → Memory tab
- Linux: Open terminal → `sudo dmidecode --type memory`

---

## Battery identification & compatibility

### Visual identification (Laptop batteries)
- **Removable:** Has a release latch on bottom, slides out without tools
- **Internal:** No visible latch, requires opening bottom panel to access

### Physical location inside laptop
- Usually the LARGEST rectangular component when you open the bottom panel
- Located toward the FRONT of the laptop (near the touchpad side)
- Has a cable with a white or black connector going to the motherboard
- May have warning labels or a barcode/model number sticker

### Compatibility quick check
**Before purchasing, verify:**
1. Battery model number (printed on old battery, e.g., "PA5024U-1BRS")
2. Voltage (V): Must match exactly (e.g., 10.8V, 11.1V, 14.8V)
3. Capacity (Wh or mAh): Can be higher for longer runtime, but check physical size fits
4. Connector type: 2-pin, 3-pin, 4-pin (must match motherboard connector)

**Warning labels to respect:**
- "Do not remove" stickers may void warranty
- Built-in batteries in ultrabooks often require authorized service

---

## SSD identification & compatibility

### Visual identification

**2.5" SATA SSD (most common for older laptops/desktops):**
- Size: 2.5 inch drive (same as laptop HDD)
- Connectors: L-shaped SATA data port + wider SATA power port
- Thickness: 7mm (standard) or 9.5mm (check laptop bay clearance)

**M.2 SATA SSD:**
- Size: 22mm wide, lengths vary: 2242 (42mm), 2260 (60mm), 2280 (80mm most common)
- Connector: 2 notches (B+M key)
- Looks like a small circuit board/stick of gum

**M.2 NVMe SSD (fastest):**
- Size: 22mm wide, 2280 length most common
- Connector: 1 notch (M key only)
- Identical appearance to M.2 SATA, check notch position to differentiate

### Physical location inside laptop
- **2.5" SSD:** In a caddy/tray, usually near the front-left or bottom of laptop, held by 4 screws (2 per side)
- **M.2 SSD:** Lies FLAT on motherboard, secured by a single screw at the far end, often has a heatsink on top

### Compatibility quick check
**Before purchasing, verify:**
1. Interface: SATA III (6Gb/s) vs NVMe PCIe Gen3/Gen4
2. Form factor: 2.5" vs M.2, and M.2 length (2280, 2260, 2242)
3. Key type for M.2: B-key (SATA), M-key (NVMe), or B+M (compatible with both)
4. Slot availability: Some laptops have only one M.2 slot; check if occupied
5. BIOS/motherboard support: Older systems may not support NVMe (only M.2 SATA)

**How to check current SSD:**
- Windows: Device Manager → Disk drives (shows model) or use CrystalDiskInfo (free)
- macOS: Apple logo → About This Mac → Storage or System Report → SATA/NVMe
- Linux: Open terminal → `lsblk` or `sudo nvme list`

---

## WiFi card identification & compatibility

### Visual identification
- **M.2 WiFi card (modern, 2016+):**
  - Size: 22mm wide x 30mm long (M.2 2230 form factor)
  - Connector: Single M.2 edge connector with one notch (E-key or A-key)
  - Has 2-4 gold circular antenna connectors on the card edge
  - Usually labeled with brand (Intel, Qualcomm, Realtek) and model

- **Mini PCIe WiFi card (older, pre-2016):**
  - Size: ~30mm x 50mm rectangular card
  - Connector: Mini PCIe edge connector
  - Has 2 antenna connectors (usually white and black wires)

### Physical location inside laptop
- **Usually located near the BOTTOM-RIGHT or BOTTOM-LEFT corner** when you open the panel
- Look for 2 thin antenna wires (white and black, or labeled MAIN/AUX) going to a small card
- May be under a piece of tape or shielding

### Compatibility quick check
**Before purchasing, verify:**
1. Form factor: M.2 2230 (modern) vs Mini PCIe (older)
2. Key type: M.2 E-key (WiFi/BT) or A-key (WiFi only)
3. WiFi standard: WiFi 5 (ac), WiFi 6 (ax), WiFi 6E, WiFi 7
4. Bluetooth version: 4.2, 5.0, 5.1, 5.2, 5.3
5. OS driver support: Ensure drivers exist for Windows/Linux/macOS
6. Whitelist: Some laptops (especially older HP/Lenovo) have a "BIOS whitelist" that only allows specific WiFi cards

**How to check current WiFi card:**
- Windows: Device Manager → Network adapters (shows exact model)
- macOS: Apple logo → About This Mac → System Report → Wi-Fi
- Linux: Open terminal → `lspci | grep -i network` or `lsusb`

**Antenna cable colors (standard):**
- White or labeled "1" / "MAIN" → Primary antenna (connector 1)
- Black or labeled "2" / "AUX" → Secondary antenna (connector 2)

---

## Screw types & sizes (common across hardware upgrades)

### Common screw sizes
- **Phillips #0:** Very small screws (WiFi cards, M.2 SSDs)
- **Phillips #1:** Most laptop/desktop case screws, battery screws
- **Phillips #2:** Larger desktop case screws, drive bay screws
- **Torx T5:** Some laptops (especially MacBooks, Surface devices)

### Screw organization tip
**When removing screws:**
1. Take a photo of the component BEFORE removing screws (for reference)
2. Use a magnetic tray OR place screws on masking tape and label positions
3. For different screw lengths: separate them or note which holes they came from

### Stuck screw emergency fix
1. Ensure screwdriver is correct size and fully seated in screw head
2. Press DOWN firmly while turning counter-clockwise
3. If stripped: place a rubber band between screwdriver and screw head for grip
4. Last resort: use a screw extractor bit (available at hardware stores)

---

## Tools recommended for hardware upgrades

### Essential tools
- Phillips #0 and #1 screwdriver set
- Anti-static wrist strap OR frequent grounding habit
- Plastic spudger or old credit card (for prying panels)
- Good lighting (desk lamp or headlamp)
- Magnetic parts tray or small containers

### Nice to have
- Torx T5 screwdriver (for some laptops)
- Compressed air (for cleaning dust)
- Isopropyl alcohol 90%+ and lint-free cloth (for cleaning contacts)
- Thermal paste (if replacing CPU cooler or heatsink)

---

## Safety & workspace setup

### Workspace requirements
1. **Flat, stable surface:** Table or desk with non-conductive mat
2. **Good lighting:** Overhead light + desk lamp to see small components
3. **No carpets:** Work on hard floor or use anti-static mat (carpets generate static)
4. **Organize:** Keep screws, old components, and tools separated

### Grounding best practices
- **Best:** Anti-static wrist strap clipped to bare metal part of PC case
- **Good:** Touch metal case/chassis every 30 seconds before handling components
- **Avoid:** Wearing wool/synthetic clothing, working on carpet, touching gold contacts

### What NOT to do
- Do NOT work on a PC while it's plugged in
- Do NOT force components into slots (check orientation first)
- Do NOT touch circuit board chips or gold contacts with bare hands
- Do NOT use magnetic screwdrivers near hard drives (OK for SSDs)
- Do NOT remove warranty stickers if device is under warranty

---

## Agent behavior when using this reference
- Ask user to identify their component type FIRST (send photo if uncertain)
- Confirm compatibility BEFORE instructing user to open device
- Reference visual cues ("look for the white cable on the left") when guiding
- If user cannot identify component from description, request a photo and describe what you see
