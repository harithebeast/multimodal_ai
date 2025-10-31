# Troubleshooting & common issues — hardware upgrades

## Purpose
This document provides quick troubleshooting steps and common failure modes for RAM, battery, SSD, and WiFi card upgrades. The agent should reference these when a user reports an error or unexpected behavior during the upgrade process.

---

## RAM UPGRADE — Troubleshooting

### Issue: PC won't boot / no display after RAM installation
**Symptoms:** Black screen, fans spin, no POST beep, or series of beeps
**Step-by-step fix:**
1. "Power off completely and unplug the power cable."
2. "Open the case again and reseat the RAM: press the clips, remove the module, and reinstall it firmly until both clips click."
3. "If still no boot, try installing only ONE RAM stick in the FIRST slot (closest to the CPU)."
4. "Boot with that single stick. Does it work? Reply 'yes' or 'no'."
5. If yes: "The other slot or second stick may be faulty. Try the second stick alone in the same slot."
6. If no: "The RAM may be incompatible or faulty. Reinstall your old RAM and confirm the PC boots normally."

### Issue: PC boots but shows less RAM than installed
**Symptoms:** Windows shows 8GB when you installed 16GB
**Step-by-step fix:**
1. "Open Task Manager → Performance → Memory. What does it say for 'Available' and 'Hardware reserved'?"
2. If large amount is 'Hardware reserved': "Restart and enter BIOS (press Del or F2 during boot). Look for 'Memory Remapping' or 'Memory Hole' option and ENABLE it."
3. "Also confirm Windows is 64-bit: press Windows key + Pause, check 'System type'. If it says '32-bit', that's your limit (4GB max usable)."

### Issue: Random crashes or blue screens after RAM installation
**Symptoms:** System freezes, BSOD with MEMORY_MANAGEMENT error
**Step-by-step fix:**
1. "Run Windows Memory Diagnostic: press Windows key, type 'memory diagnostic', and select 'Restart now and check for problems'."
2. "Let it run for at least one full pass (5-10 minutes). When it finishes, Windows will show results."
3. If errors found: "One or both RAM sticks are faulty. Try each stick individually to isolate the bad one."
4. If no errors but still crashes: "RAM may be running at wrong speed. Enter BIOS → enable XMP/DOCP profile OR manually set RAM speed to match the rated speed (e.g., 3200MHz)."

---

## BATTERY REPLACEMENT — Troubleshooting

### Issue: Laptop won't power on after battery replacement
**Step-by-step fix:**
1. "Remove the new battery completely."
2. "Plug in ONLY the AC adapter (no battery installed)."
3. "Press power button. Does laptop turn on? Reply 'yes' or 'no'."
4. If yes: "The new battery may be defective or not making good contact. Reinstall battery, ensuring connector is fully seated and latch is locked."
5. If no: "You may have accidentally disconnected another cable. Open the panel again and check that all connectors near the battery (especially the main power connector to motherboard) are firmly seated."

### Issue: Battery not charging / shows 0% or 'plugged in, not charging'
**Step-by-step fix:**
1. "Check Windows battery settings: right-click battery icon → Power Options → check if battery saver mode is on (turn it off)."
2. "Restart laptop and check again. Still not charging? Reply 'yes' or 'no'."
3. If yes: "The battery may need calibration. Fully charge to 100%, then use laptop until it shuts down at 0%. Charge back to 100% without interruption."
4. "If still not charging after calibration, the battery may be defective (request RMA/replacement from seller)."

---

## SSD REPLACEMENT — Troubleshooting

### Issue: SSD not detected in BIOS / boot menu
**Symptoms:** New SSD doesn't appear in BIOS or Disk Management
**Step-by-step fix (2.5" SATA SSD):**
1. "Power off and open case again."
2. "Check SATA data cable is firmly connected to BOTH the SSD and the motherboard SATA port (push in until you feel a click)."
3. "Check SATA power cable is firmly connected to the SSD power port."
4. "Try a DIFFERENT SATA port on the motherboard (they are numbered: SATA0, SATA1, etc.)."
5. "Boot to BIOS. Does SSD appear now? Reply 'yes' or 'no'."

**Step-by-step fix (M.2 NVMe SSD):**
1. "Power off and open the panel."
2. "Remove the M.2 SSD and inspect the contacts (gold fingers). Are they clean and not damaged?"
3. "Reinsert the SSD firmly into the M.2 slot, ensuring the notch aligns with the key."
4. "Press down and tighten the screw."
5. "Boot to BIOS → look for 'M.2 Configuration' or 'PCIe Configuration'. Ensure the M.2 slot is set to 'NVMe' mode (not SATA mode)."
6. "Does SSD appear now? Reply 'yes' or describe what you see."

### Issue: SSD detected but very slow performance
**Step-by-step fix:**
1. "Open Device Manager (right-click Start → Device Manager)."
2. "Expand 'Disk drives', right-click your SSD, select Properties → Policies tab."
3. "Ensure 'Enable write caching' is checked."
4. "For NVMe: check that the SSD is in a PCIe x4 slot (not x2). In BIOS, look for 'M.2 Slot Bandwidth' — should say 'x4'."

---

## WIFI CARD REPLACEMENT — Troubleshooting

### Issue: No WiFi networks found / adapter not detected
**Symptoms:** Network menu shows "No WiFi adapter found" or airplane mode stuck
**Step-by-step fix:**
1. "Power off and open panel again."
2. "Check both antenna cables are firmly pressed onto the WiFi card's gold connectors. You should feel a small click."
3. "Check WiFi card is fully inserted into M.2 slot and screw is tight."
4. "Boot to Windows. Open Device Manager → Network adapters. Do you see the WiFi card listed (may have a yellow exclamation mark)? Reply 'yes' or 'no'."
5. If yes with exclamation: "Right-click the WiFi adapter → Update driver → Search automatically. Or download driver from WiFi card manufacturer's website."
6. If not listed at all: "The card may not be compatible with your laptop's M.2 slot (some slots are SATA-only, not PCIe). Check your laptop's service manual for WiFi card compatibility."

### Issue: WiFi works but signal is very weak
**Step-by-step fix:**
1. "Power off and check antenna cables are on the CORRECT connectors: white (MAIN/1) and black (AUX/2). Swap them if reversed."
2. "Ensure antennas are not pinched or damaged when you closed the panel."
3. "Check that antenna cables are routed along the edge of the laptop (not folded or kinked)."

---

## General safety reminders (all procedures)
- **Before opening ANY device:** Power off completely, unplug AC adapter, remove battery (if possible), and discharge residual power by holding power button for 10-15 seconds.
- **Always ground yourself** before touching components (wrist strap or touch metal chassis).
- **Keep screws organized** — use a magnetic tray or take a photo of screw locations.
- **Do not force connectors** — if a cable or module doesn't slide in easily, check orientation/alignment.
- **If stuck screw:** Do NOT strip it. Use correct screwdriver size, apply firm downward pressure while turning, or use a rubber band for grip.

---

## Agent escalation rules
- If user reports physical damage (broken clip, bent pin, cracked PCB): STOP procedure and advise contacting professional repair or manufacturer support.
- If multiple remediation attempts fail (e.g., tried 3 fixes and still no boot): Suggest restoring original component and seeking professional help.
- If user is uncomfortable at any step: Pause and offer to explain further, or suggest taking device to a repair shop.
