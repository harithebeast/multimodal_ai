# Hardware upgrade assistant — precise step-by-step guide

## Purpose
This document provides extremely detailed, visual, step-by-step hardware upgrade procedures for:
- RAM replacement/upgrade
- Battery replacement
- SSD replacement/upgrade
- WiFi card replacement

Each step includes precise physical instructions (e.g., "remove the left screw") and verification checkpoints. The agent must present one step at a time and wait for user confirmation before proceeding.

---

# RAM REPLACEMENT / UPGRADE

## Tools needed
- Phillips #0 or #1 screwdriver
- Anti-static wrist strap (or frequent chassis grounding)
- Clean workspace with good lighting
- Plastic spudger or guitar pick (optional, for prying panels)

## Pre-flight checks
- Confirm new RAM is compatible: same type (DDR4/DDR5), correct form factor (SO-DIMM for laptops, DIMM for desktops), matching or compatible speed
- Backup all important data
- Confirm you are authorized to open the device

## Step-by-step: RAM upgrade (Desktop PC)

1. **Power down completely**
   - Instruction: "Shut down Windows/macOS/Linux using the normal shutdown procedure. Once off, flip the power supply switch on the back of the case to the OFF position (O symbol). Unplug the main power cable from the wall outlet."
   - Verification: "Is the power cable unplugged and the PSU switch set to OFF? Reply 'yes' to continue."

2. **Discharge residual power**
   - Instruction: "Press and hold the front power button for 10 seconds to drain any remaining charge from the motherboard."
   - Verification: "Done? Reply 'yes'."

3. **Open the case — remove left side panel**
   - Instruction: "Place the PC on its right side so the left panel faces up. Look at the rear of the case: you'll see 2 thumb screws or Phillips screws holding the left panel. Remove these screws (turn counter-clockwise). Slide the panel backward about 1 inch, then lift it off."
   - Verification: "Can you see the motherboard and components inside? Reply 'yes' or send a photo."

4. **Ground yourself**
   - Instruction: "Put on an anti-static wrist strap and clip it to the metal chassis, or touch the metal case frame for 5 seconds before touching any components."
   - Verification: "Grounded? Reply 'yes'."

5. **Locate the RAM slots**
   - Instruction: "Find the RAM slots on the motherboard. They are usually near the CPU (tall heatsink or fan) and have 2 or 4 long vertical slots with clips on each end. The RAM sticks stand vertically and have a small notch off-center."
   - Verification: "Do you see the RAM slots and the clips at each end? Reply 'yes' or describe what you see."

6. **Remove old RAM (if replacing)**
   - Instruction: "At each end of the RAM stick, push the plastic retention clip OUTWARD (away from the RAM). The stick will pop up slightly. Grasp the RAM by its edges (not the gold contacts) and pull straight up to remove it. Place it on an anti-static bag or non-conductive surface."
   - Verification: "Old RAM removed and set aside safely? Reply 'yes'."

7. **Install new RAM**
   - Instruction: "Hold the new RAM stick by its edges. Align the notch in the RAM with the key in the slot (the notch is off-center, so it only fits one way). Position the RAM above the slot and press down firmly and evenly on both ends until you hear a CLICK and both clips snap into place automatically."
   - Verification: "Do both clips at the ends snap closed and hold the RAM firmly? The module should be seated flat and not tilted. Reply 'yes' or 'no'."

8. **Close the case**
   - Instruction: "Slide the left panel back on (align the rail, slide forward, then replace the 2 screws). Tighten screws finger-tight."
   - Verification: "Panel reinstalled? Reply 'yes'."

9. **Reconnect power and boot**
   - Instruction: "Plug the power cable back into the wall, flip the PSU switch to ON (I symbol), and press the front power button."
   - Verification: "Does the PC power on and show the manufacturer logo or reach the Windows/BIOS screen? Reply 'yes' or describe any beeps/error messages."

10. **Verify RAM in operating system**
    - Instruction: "Once in Windows: press Ctrl+Shift+Esc to open Task Manager, click 'Performance' tab, then 'Memory'. Check the total RAM shown at the top right. On macOS: click Apple logo → About This Mac. On Linux: open terminal and run 'free -h'."
    - Verification: "What is the total RAM displayed? Does it match your expected amount (e.g., 16GB)?"

11. **Run memory test (optional but recommended)**
    - Instruction: "Press Windows key, type 'Windows Memory Diagnostic', and run it. It will reboot and test RAM for 5-10 minutes. OR use MemTest86 for a more thorough test."
    - Verification: "Did the test complete with no errors? Reply 'yes' or share the error count."

## Step-by-step: RAM upgrade (Laptop)

1. **Power down and remove battery (if removable)**
   - Instruction: "Shut down the laptop. Unplug the AC adapter. If your laptop has a removable battery: flip the laptop over, slide the battery release latch to the UNLOCK position, and lift the battery out."
   - Verification: "Laptop off, unplugged, battery removed (if applicable)? Reply 'yes'."

2. **Discharge residual power**
   - Instruction: "Press and hold the power button for 15 seconds."
   - Verification: "Done? Reply 'yes'."

3. **Remove bottom panel or memory hatch**
   - Instruction: "Flip laptop upside down. Look for a small rectangular access panel (usually marked with a RAM icon) OR you may need to remove the entire bottom cover. Count the screws: typically 8-12 small Phillips screws around the perimeter. Remove all screws and place them in a container. Use a plastic spudger or guitar pick to gently pry the panel starting from a corner notch. Work around the edges until it pops free."
   - Verification: "Panel removed and you can see the RAM slots? Reply 'yes' or send a photo."

4. **Ground yourself**
   - Instruction: "Touch the metal chassis or any unpainted metal part for 5 seconds."
   - Verification: "Grounded? Reply 'yes'."

5. **Identify RAM orientation**
   - Instruction: "Look at the RAM module: it sits at roughly a 30-degree angle. Note the small notch in the gold contacts (off-center)."
   - Verification: "Can you see the notch and the clips at each side? Reply 'yes'."

6. **Remove old RAM**
   - Instruction: "Gently pull the metal clips at the LEFT and RIGHT sides of the RAM module OUTWARD at the same time. The module will pop up to about a 30-degree angle. Grasp it by the edges and slide it OUT of the slot."
   - Verification: "Old module removed? Reply 'yes'."

7. **Install new RAM**
   - Instruction: "Hold new RAM at a 30-degree angle, align the notch with the key in the slot, and slide it INTO the slot firmly. Then press down on the top edge until it clicks flat and the side clips snap into place."
   - Verification: "RAM seated flat and clips locked? Reply 'yes' or 'no'."

8. **Replace bottom panel**
   - Instruction: "Align the panel with the screw holes, press it down gently, and replace all screws in reverse order (start with corners, then edges)."
   - Verification: "Panel secured? Reply 'yes'."

9. **Reinstall battery (if removable) and boot**
   - Instruction: "Slide battery back in and lock the latch. Plug in AC adapter and press the power button."
   - Verification: "Laptop boots to logo or OS? Reply 'yes' or describe beeps/errors."

10. **Verify RAM recognized**
    - Instruction: "In Windows: Ctrl+Shift+Esc → Performance → Memory. On macOS: Apple → About This Mac. On Linux: 'free -h'."
    - Verification: "What total RAM is shown? Does it match expected?"

---

# BATTERY REPLACEMENT (Laptop)

## Tools needed
- Phillips #0 screwdriver
- Plastic spudger or guitar pick
- Replacement battery (confirm model compatibility)

## Step-by-step: Battery replacement (Removable battery)

1. **Power down and unplug**
   - Instruction: "Shut down laptop completely. Unplug AC adapter."
   - Verification: "Laptop off and unplugged? Reply 'yes'."

2. **Release battery latch**
   - Instruction: "Flip laptop upside down. Locate the battery release latch (usually a sliding switch near the battery). Slide it to the UNLOCK or RELEASE position and hold it there."
   - Verification: "Latch moved to unlock? Reply 'yes'."

3. **Remove old battery**
   - Instruction: "While holding the latch, use your other hand to lift the battery straight out of the compartment."
   - Verification: "Old battery removed? Reply 'yes'."

4. **Inspect battery contacts**
   - Instruction: "Look at the metal contacts inside the battery bay. They should be clean and not bent. If dusty, gently wipe with a dry cloth."
   - Verification: "Contacts look clean? Reply 'yes'."

5. **Install new battery**
   - Instruction: "Align the new battery's contacts with the bay contacts. Slide the battery in at a slight angle, then press down firmly until you hear a click and the latch snaps to the LOCKED position."
   - Verification: "Battery seated and latch locked? Gently tug the battery to confirm it's secure. Reply 'yes'."

6. **Plug in and test**
   - Instruction: "Plug in the AC adapter and press the power button."
   - Verification: "Laptop boots normally? Check battery icon in taskbar — does it show charging? Reply with battery percentage shown."

## Step-by-step: Battery replacement (Internal/non-removable battery)

1. **Power down and unplug**
   - Instruction: "Shut down laptop. Unplug AC adapter."
   - Verification: "Off and unplugged? Reply 'yes'."

2. **Discharge power**
   - Instruction: "Press and hold power button for 15 seconds."
   - Verification: "Done? Reply 'yes'."

3. **Remove bottom panel**
   - Instruction: "Flip laptop over. Remove all visible screws from the bottom panel (count them — typically 8-12). Some screws may be hidden under rubber feet; gently pry feet with a spudger. After screws are out, use a plastic spudger to pry around the edge of the panel starting from a notch or corner. Work slowly until the panel pops off."
   - Verification: "Bottom panel removed and you can see the internal battery (usually a large rectangular component with a cable connector)? Reply 'yes' or send photo."

4. **Disconnect battery cable**
   - Instruction: "Locate the battery connector on the motherboard. It's a small white or black plastic plug with wires going to the battery. Gently pull the connector STRAIGHT UP using a plastic spudger or your fingers. Do NOT pull on the wires."
   - Verification: "Battery connector unplugged from motherboard? Reply 'yes'."

5. **Remove battery mounting screws**
   - Instruction: "Look for 3-6 small Phillips screws holding the battery to the chassis. Remove these screws."
   - Verification: "Screws removed? Reply 'yes'."

6. **Lift out old battery**
   - Instruction: "Carefully lift the old battery out of the laptop. If it has adhesive, gently pry from one corner with a spudger."
   - Verification: "Old battery removed? Reply 'yes'."

7. **Install new battery**
   - Instruction: "Place the new battery in the same position. If your new battery came with adhesive strips, peel the backing and press the battery down firmly. Replace the mounting screws."
   - Verification: "New battery secured with screws? Reply 'yes'."

8. **Reconnect battery cable**
   - Instruction: "Align the battery connector with the motherboard socket and press down firmly until it clicks into place."
   - Verification: "Connector seated? Reply 'yes'."

9. **Replace bottom panel and boot**
   - Instruction: "Align panel, press down, replace all screws. Plug in AC adapter and press power button."
   - Verification: "Laptop boots? Battery icon shows charging? Reply with battery status."

---

# SSD REPLACEMENT / UPGRADE

## Tools needed
- Phillips #0 or #1 screwdriver
- Plastic spudger (for laptops)
- Anti-static wrist strap
- Replacement SSD (confirm interface: M.2 NVMe, M.2 SATA, or 2.5" SATA)

## Step-by-step: SSD replacement (Desktop — 2.5" SATA)

1. **Power down and open case**
   - Instruction: "Follow RAM replacement steps 1-3 above to power down, discharge, and open the left side panel."
   - Verification: "Case open? Reply 'yes'."

2. **Locate existing SSD/HDD**
   - Instruction: "Find the drive bay (usually front or bottom of case). You'll see a 2.5" or 3.5" drive held by screws or a tool-less bracket."
   - Verification: "Drive located? Reply 'yes'."

3. **Disconnect SATA and power cables**
   - Instruction: "At the back of the drive, pull the L-shaped SATA data cable straight out. Then pull the wider power cable (4-pin or SATA power) straight out."
   - Verification: "Both cables disconnected? Reply 'yes'."

4. **Remove drive from bay**
   - Instruction: "Remove 4 screws (2 on each side of the drive) holding it to the bay or bracket. Slide the drive out."
   - Verification: "Old drive removed? Reply 'yes'."

5. **Install new SSD**
   - Instruction: "Slide new SSD into the bay. Align screw holes and replace the 4 screws (finger-tight)."
   - Verification: "SSD mounted? Reply 'yes'."

6. **Connect SATA and power cables**
   - Instruction: "Connect SATA data cable (from motherboard) to the SSD's SATA port. Connect SATA power cable (from PSU) to the SSD's power port. Both should click in."
   - Verification: "Cables connected firmly? Reply 'yes'."

7. **Close case and boot**
   - Instruction: "Replace side panel, plug in power, boot PC."
   - Verification: "PC boots? If SSD has OS, does it boot to Windows/Linux? If blank, do you see it in BIOS under boot devices? Reply 'yes' or describe."

## Step-by-step: SSD replacement (Laptop — M.2 NVMe)

1. **Power down and remove battery**
   - Instruction: "Follow Battery Replacement steps 1-3 to power off, discharge, and open the bottom panel."
   - Verification: "Bottom panel removed? Reply 'yes'."

2. **Locate M.2 SSD slot**
   - Instruction: "Look for a small card (about 22mm wide, 80mm long) lying flat on the motherboard, secured by a single screw at the far end. It may have a label or heatsink on top."
   - Verification: "M.2 SSD located? Reply 'yes' or send photo."

3. **Remove heatsink (if present)**
   - Instruction: "If there's a metal or thermal pad on top, remove 1-2 small screws holding it and lift it off."
   - Verification: "Heatsink removed or not present? Reply 'yes'."

4. **Remove retaining screw**
   - Instruction: "At the far end of the M.2 card (opposite the connector), remove the single small Phillips screw. Keep this screw safe."
   - Verification: "Screw removed? Reply 'yes'."

5. **Remove old M.2 SSD**
   - Instruction: "The SSD will pop up at a 30-degree angle. Gently pull it straight OUT of the M.2 socket."
   - Verification: "Old SSD removed? Reply 'yes'."

6. **Install new M.2 SSD**
   - Instruction: "Hold new SSD at a 30-degree angle. Align the notch with the key in the M.2 slot and slide it IN until fully seated. Press down flat and replace the retaining screw at the far end."
   - Verification: "SSD seated flat and screw tightened? Reply 'yes'."

7. **Replace heatsink (if applicable)**
   - Instruction: "If you removed a heatsink, place it back on top and replace its screws."
   - Verification: "Heatsink reinstalled? Reply 'yes'."

8. **Close panel and boot**
   - Instruction: "Replace bottom panel, screws, battery (if removable), plug in AC, and power on."
   - Verification: "Laptop boots? Do you see SSD in BIOS or does OS load? Reply 'yes' or describe."

---

# WIFI CARD REPLACEMENT

## Tools needed
- Phillips #0 screwdriver
- Plastic spudger
- Replacement WiFi card (confirm interface: M.2 2230, Mini PCIe, or specific model)

## Step-by-step: WiFi card replacement (Laptop — M.2 WiFi card)

1. **Power down and open bottom panel**
   - Instruction: "Follow Battery Replacement steps 1-3 to power down, discharge, and remove bottom panel."
   - Verification: "Panel removed? Reply 'yes'."

2. **Locate WiFi card**
   - Instruction: "Find the WiFi card (small M.2 card, usually near a corner, about 22mm x 30mm). It has 2 thin antenna cables (black and white or labeled MAIN and AUX) connected to it."
   - Verification: "WiFi card located? Reply 'yes' or send photo."

3. **Disconnect antenna cables**
   - Instruction: "Gently pry the antenna cable connectors OFF the WiFi card using a plastic spudger or your fingernail. Pull STRAIGHT UP. Note which cable goes to which connector (usually white = MAIN, black = AUX, or labeled 1 and 2)."
   - Verification: "Both antenna cables disconnected? Reply 'yes'."

4. **Remove WiFi card retaining screw**
   - Instruction: "Remove the single small screw at the end of the WiFi card."
   - Verification: "Screw removed? Reply 'yes'."

5. **Remove old WiFi card**
   - Instruction: "The card will pop up to ~30 degrees. Gently pull it OUT of the M.2 slot."
   - Verification: "Old WiFi card removed? Reply 'yes'."

6. **Install new WiFi card**
   - Instruction: "Hold new card at 30-degree angle, align notch with M.2 key, slide IN until fully inserted. Press down flat and replace screw."
   - Verification: "New card seated and screw tight? Reply 'yes'."

7. **Reconnect antenna cables**
   - Instruction: "Press the antenna connectors onto the new card's gold connectors. White (MAIN) usually goes to connector 1, black (AUX) to connector 2. Press down until you feel a small click."
   - Verification: "Antennas reconnected? Reply 'yes'."

8. **Close panel and boot**
   - Instruction: "Replace bottom panel and screws. Power on laptop."
   - Verification: "Laptop boots? Can you see WiFi networks in the network menu? Reply 'yes' or describe."

9. **Install drivers (if needed)**
   - Instruction: "Windows may auto-detect the card. If not, download drivers from the WiFi card manufacturer's website or use the installation CD."
   - Verification: "WiFi working and able to connect to a network? Reply 'yes'."

---

## Agent behavior requirements (applies to ALL procedures above)
- Present exactly ONE step at a time.
- After each instruction, WAIT for user confirmation (yes/no, photo, or reported value) before moving to the next step.
- If user reports failure, stuck screw, or unexpected result: STOP, provide one concise remediation instruction, and ask user to retry verification before proceeding.
- Keep language conversational but extremely precise with physical details.
- Always confirm grounding before touching components.
- Always remind user to keep screws organized and take photos if unsure.