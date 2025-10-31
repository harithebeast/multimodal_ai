# Advanced Procedures & Post-Installation

## Purpose
Advanced steps after hardware installation: BIOS configuration, driver installation, performance testing, and optimization.

---

## BIOS/UEFI Configuration

### When to Access BIOS
**Access BIOS after installing:**
- New RAM (to enable XMP/DOCP for faster speeds)
- New SSD (to verify boot order, enable NVMe support)
- Any component that isn't being detected

**How to enter BIOS:**
1. "Power on the computer"
2. "Immediately press the BIOS key repeatedly (every second)"
3. Common keys by manufacturer:
   - **Dell:** F2 or F12
   - **HP:** F10 or Esc
   - **Lenovo:** F1 or F2
   - **ASUS:** F2 or Delete
   - **Acer:** F2 or Delete
   - **MSC:** Delete
   - **Generic/Custom PC:** Delete or F2

**If you miss it:**
- Restart and try again
- Look for "Press [key] to enter setup" message during boot

### RAM Configuration in BIOS

**Enable XMP/DOCP for full RAM speed:**
1. "Enter BIOS (F2, Delete, or F10 depending on manufacturer)"
2. "Navigate to 'Advanced' or 'Overclocking' or 'AI Tweaker' tab"
3. "Find setting called 'XMP' (Intel) or 'DOCP/EXPO' (AMD)"
4. "Change from 'Disabled' to 'Profile 1' or 'Enabled'"
5. "Press F10 to save and exit"

**Why this matters:**
- RAM defaults to base speed (e.g., 2133 MHz)
- XMP enables advertised speed (e.g., 3200 MHz)
- Can improve performance by 10-20%

**Check RAM in BIOS:**
- Look for "Memory Information" or "System Information"
- Should show: Total capacity, speed, number of sticks
- Verify all RAM is detected (e.g., 2x8GB = 16GB total)

**If RAM not detected or showing less than installed:**
1. "Power off, unplug, reseat RAM sticks (remove and reinstall firmly)"
2. "Try one stick at a time in slot closest to CPU"
3. "Check motherboard manual for correct slot configuration"

### SSD Configuration in BIOS

**Verify SSD is detected:**
1. "Enter BIOS"
2. "Navigate to 'Storage Configuration' or 'SATA Configuration' or 'Boot' tab"
3. "Look for list of connected drives"
4. "New SSD should appear in list (shows model number)"

**If SSD not detected:**
1. "Check 'SATA Mode' is set to 'AHCI' (not IDE or RAID unless needed)"
2. "For M.2 NVMe: check if 'NVMe Support' is enabled"
3. "Some motherboards disable M.2 slot when certain SATA ports are used (check manual)"

**Set boot order (if installing OS on new SSD):**
1. "Navigate to 'Boot' or 'Boot Priority' tab"
2. "Move new SSD to first position in boot order"
3. "Disable or move old drive to second position"
4. "Save and exit (F10)"

**Enable AHCI mode (for best SSD performance):**
- Should already be enabled on modern systems
- Changing from IDE to AHCI on existing Windows requires registry edit (advanced)
- New installations: ensure AHCI is selected before installing Windows

### WiFi Card Configuration in BIOS

**Most WiFi cards work automatically, but check if:**
- Card not detected in Windows Device Manager
- BIOS whitelist error appears (older HP/Lenovo laptops)

**Whitelist bypass (advanced, use with caution):**
1. Some older laptops have BIOS whitelist (only allow specific WiFi cards)
2. Error message: "Unauthorized wireless card detected"
3. Solutions:
   - Buy whitelisted card (check laptop support forum for compatible models)
   - Update BIOS to latest version (may remove whitelist)
   - Modified BIOS (RISKY, can brick laptop — only for experts)

**Disable Secure Boot (if WiFi card not detected):**
1. "Enter BIOS"
2. "Navigate to 'Security' or 'Boot' tab"
3. "Find 'Secure Boot' and set to 'Disabled'"
4. "Save and exit"
5. Try again (some cards need Secure Boot off)

---

## Driver Installation

### Windows Driver Installation

**RAM:** No drivers needed

**SSD:** 
- Windows 10/11 includes NVMe drivers (usually works automatically)
- For best performance, install manufacturer driver:
  - Samsung: Samsung Magician software
  - WD: WD Dashboard
  - Crucial: Crucial Storage Executive

**WiFi Card:**
1. "After installing card and booting Windows, open Device Manager"
2. "Expand 'Network adapters' section"
3. "Look for WiFi card name (may show as 'Unknown device' with yellow triangle)"
4. "Right-click → 'Update driver' → 'Search automatically'"
5. If Windows doesn't find driver:
   - Go to manufacturer website (Intel, Qualcomm, Realtek)
   - Download driver for your exact card model
   - Install manually

**How to find WiFi card model:**
- Device Manager → Network adapters → right-click → Properties → Details → Hardware IDs
- Note the VEN (vendor) and DEV (device) codes
- Search online: "VEN_XXXX DEV_YYYY driver"

### macOS Driver Installation

**RAM/SSD:** macOS includes drivers, no action needed

**WiFi Card:**
- Official Apple WiFi cards: work automatically
- Third-party cards (Broadcom, Intel): may need kext (kernel extension)
- Search community forums for your specific card model + macOS version

### Linux Driver Installation

**RAM/SSD:** Kernel includes drivers, works automatically

**WiFi Card:**
1. "Open terminal"
2. "Check if detected: `lspci | grep -i network`"
3. "Check if driver loaded: `lsmod | grep -i wifi`"
4. If not working:
   - Intel cards: usually work out-of-box
   - Realtek: may need `rtw88` or `rtw89` driver
   - Broadcom: may need `broadcom-wl` driver
   - Install via package manager: `sudo apt install firmware-realtek` (example)

---

## Performance Testing & Verification

### RAM Testing

**Quick test (Windows):**
1. "Press Windows key + Pause"
2. "Check 'Installed RAM' matches what you installed"
3. "Open Task Manager → Performance → Memory"
4. "Verify speed shows correctly (e.g., 3200 MHz if you enabled XMP)"

**Thorough test (check for errors):**
1. "Download MemTest86 (free) or use Windows Memory Diagnostic"
2. "Run test for at least one full pass (1-2 hours)"
3. "ANY errors = bad RAM stick or incompatibility"
4. If errors found: test sticks individually to identify faulty one

**Performance benchmark:**
- Download AIDA64 or CPU-Z
- Check read/write/copy speeds
- Compare to spec sheet for your RAM

### Battery Testing

**Check battery health (Windows):**
1. "Open PowerShell as Administrator"
2. "Run: `powercfg /batteryreport`"
3. "Open generated HTML report (shows battery health, capacity)"
4. "Design capacity vs full charge capacity = health percentage"

**What to look for:**
- New battery should show 95-100% of design capacity
- Charge/discharge cycles should be low (0-10 for new battery)
- If significantly less than design capacity: battery may be old stock or defective

**Runtime test:**
1. "Charge to 100%"
2. "Disconnect charger and use normally"
3. "Note time until low battery warning (10%)"
4. "Compare to manufacturer's rated battery life"

### SSD Testing

**Verify SSD is detected and showing correct capacity:**
1. "Windows: open Disk Management (right-click Start → Disk Management)"
2. "Look for new SSD in list"
3. "Capacity should match (e.g., 512GB SSD shows ~476GB usable)"

**Performance test:**
1. "Download CrystalDiskMark (free)"
2. "Run test on new SSD"
3. "Check sequential read/write speeds:"
   - **SATA SSD:** ~500-550 MB/s read, ~500 MB/s write
   - **NVMe Gen3:** ~3000-3500 MB/s read, ~2000-3000 MB/s write
   - **NVMe Gen4:** ~5000-7000 MB/s read, ~4000-6000 MB/s write

**If speeds are much lower:**
- Check if AHCI mode is enabled in BIOS
- Verify PCIe Gen3/Gen4 is enabled (not limited to Gen2)
- Check if SSD is in correct M.2 slot (some slots are limited to SATA speeds)

### WiFi Testing

**Check connection:**
1. "Click WiFi icon in system tray"
2. "Connect to your network"
3. "Should show signal strength and 'Connected'"

**Check speed:**
1. "Windows: Settings → Network & Internet → WiFi → Hardware properties"
2. "Look for 'Link speed' (e.g., 866 Mbps, 1200 Mbps)"
3. "Should show maximum speed for WiFi standard:"
   - WiFi 5 (ac): up to 866 Mbps
   - WiFi 6 (ax): up to 1200-2400 Mbps
   - WiFi 6E: up to 2400 Mbps

**Speed test:**
1. "Go to speedtest.net or fast.com"
2. "Run test and compare to your internet plan speed"
3. "Should get most of your rated speed (within 80%)"

**If speeds are slow:**
- Check router supports same WiFi standard (WiFi 6 card needs WiFi 6 router)
- Verify using 5GHz band (not 2.4GHz)
- Check antenna cables are properly connected
- Update WiFi drivers

---

## Optimization & Fine-Tuning

### RAM Optimization

**Disable unnecessary startup programs (free up RAM):**
1. "Open Task Manager → Startup tab"
2. "Disable programs you don't need at startup"
3. "Restart to see effect"

**Check for RAM leaks:**
1. "Open Task Manager → Performance → Memory"
2. "Note 'In use' amount after fresh boot"
3. "After several hours of use, check again"
4. "If 'In use' climbs excessively, a program may have memory leak"

### SSD Optimization (Windows)

**Enable TRIM (maintains SSD performance):**
1. "Open Command Prompt as Administrator"
2. "Run: `fsutil behavior query DisableDeleteNotify`"
3. "Should show '0' (TRIM is enabled)"
4. "If shows '1', run: `fsutil behavior set DisableDeleteNotify 0`"

**Disable hibernation (saves SSD space):**
1. "Open Command Prompt as Administrator"
2. "Run: `powercfg /hibernate off`"
3. "Frees up several GB on SSD"

**Optimize drive:**
1. "Open 'Defragment and Optimize Drives' (search in Start menu)"
2. "Select SSD and click 'Optimize'"
3. "Windows will run TRIM command"
4. "Schedule monthly optimization"

**What NOT to do with SSD:**
- Do NOT defragment (wears out SSD unnecessarily)
- Do NOT disable page file (needed for stability)
- Do NOT fill to 100% capacity (keep 10-20% free for best performance)

### Battery Optimization

**Extend battery lifespan:**
1. "Keep charge between 20-80% when possible"
2. "Avoid leaving plugged in at 100% constantly"
3. "Use battery saver mode when on battery"
4. "Some laptops have 'Battery Care' setting in BIOS (limits charge to 80%)"

**Calibrate battery (once every 3 months):**
1. "Charge to 100%"
2. "Unplug and use until fully drained (0%)"
3. "Immediately charge back to 100% without interruption"
4. "Helps battery meter show accurate percentage"

### WiFi Optimization

**Optimize WiFi settings (Windows):**
1. "Device Manager → Network adapters → WiFi card → Properties"
2. "Advanced tab → Adjust settings:"
   - **Roaming Aggressiveness:** Medium or High
   - **Transmit Power:** Highest
   - **Wireless Mode:** 802.11ac or 802.11ax (not auto if available)

**Prefer 5GHz band:**
1. "Most routers have separate 2.4GHz and 5GHz networks"
2. "Connect to 5GHz for faster speeds (shorter range)"
3. "Use 2.4GHz only if 5GHz signal is weak"

**Update router firmware:**
- Check router manufacturer's website
- Updated firmware can improve compatibility and speed

---

## Troubleshooting Post-Installation

### System won't boot after upgrade

**Possible causes:**
1. RAM not seated properly → reseat RAM
2. Battery not connected → check battery connector
3. Wrong boot order → enter BIOS and set correct drive
4. Incompatible component → remove new component and test

### Component not detected

**Checklist:**
1. Component fully seated/connected
2. BIOS set to enable component (NVMe support, SATA mode, etc.)
3. Drivers installed (WiFi especially)
4. Windows updates installed
5. Try different slot (if available)

### Performance worse than expected

**Check:**
1. Drivers up to date
2. BIOS settings correct (XMP for RAM, AHCI for SSD)
3. Background programs consuming resources
4. Thermal throttling (check temperatures with HWMonitor)

---

## When to Seek Professional Help

**Consider professional assistance if:**
- BIOS whitelist error persists
- Component repeatedly fails tests
- System unstable after multiple troubleshooting attempts
- You're uncomfortable with advanced BIOS changes
- Physical damage to laptop (cracked case, broken clips)

**What to tell technician:**
- Exact components you installed
- Steps you've taken
- Error messages or symptoms
- Results of any tests you ran
