# ESP32 Marauder (Headless CLI) - Deployment, Workflow & Auditing Guide

A technical deployment guide and operational workflow manual for running the **ESP32 Marauder Security Auditing Suite** on the **ESP32 DevKit V1 (ESP-WROOM-32)** via a Headless Serial Command Line Interface (CLI).

---

## 1. Executive Summary & Purpose

The **ESP32 Marauder** (originally developed by *JustCallMeKoko*) is an open-source wireless security analysis suite designed for micro-controllers. While often deployed alongside external touchscreen modules (such as the Flipper Zero WiFi Devboard or LilyGO T-Display), this deployment focuses on the **Headless CLI configuration** on a standard ESP32 DevKit V1 board.

In this headless setup:
* No external LCD, SD card module, or peripheral buttons are required.
* Power and data communication occur over a single USB cable.
* Operations are managed via an interactive serial terminal (115200 baud).
* Provides a cost-effective, portable laboratory environment for wireless security testing, 802.11 frame inspection, and BLE auditing.

---

## 2. Hardware Profile & Target Specifications

| Parameter | Specification |
| :--- | :--- |
| **Board Name** | ESP32 DevKit V1 (30-pin layout) |
| **Core Microprocessor** | ESP-WROOM-32 (Xtensa Dual-Core 32-bit LX6 up to 240 MHz) |
| **Flash Memory** | 4 MB SPI Flash |
| **SRAM** | 520 KB |
| **USB-to-UART Bridge** | QinHeng Electronics USB Single Serial / CP2102 |
| **Linux Device Node** | `/dev/ttyACM0` (or `/dev/ttyUSB0`) |
| **Operating Voltages** | 5V USB Input / 3.3V Logic Level |
| **Physical Controls** | `EN` (Reset) & `BOOT` (GPIO 0 Download Mode) buttons |

---

## 3. End-to-End Workflow Architecture

```mermaid
flowchart TD
    A["Phase 1: Environment & Binary Acquisition<br>Download bootloader, partitions, and Marauder CLI binaries"] --> B["Phase 2: Chip Flashing (esptool)<br>Erase Flash & write binaries to specific memory offsets"]
    B --> C["Phase 3: Hardware Initialization<br>Reboot ESP32 (EN button) & establish Serial Link @ 115200 baud"]
    C --> D["Phase 4: Security Auditing Operations<br>Execute Marauder CLI commands (Scan, Sniff, Audit, Capture)"]
```

### Workflow Breakdown

1. **Environment Preparation & Firmware Acquisition:**
   * Verify USB serial port connectivity and device permissions.
   * Acquire compatible ESP32 Marauder binary components:
     * `bootloader.bin` (Loads core system initialization at address `0x1000`)
     * `partitions.bin` (Defines SPI Flash memory partitioning at address `0x8000`)
     * `esp32_marauder_...bin` (Application binary loaded at address `0x10000`)

2. **Firmware Flashing via `esptool`:**
   * Put ESP32 into bootloader mode (`BOOT` button logic or automated DTR/RTS signalling).
   * Perform a clean erase of the SPI flash memory to eliminate lingering configurations.
   * Burn the binaries to their respective memory offsets using `esptool.py`.

3. **Reboot and Serial Terminal Connection:**
   * Press the `EN` button to boot into Marauder OS.
   * Open a serial terminal emulator at `115200` baud rate with local echo or ANSI support.

4. **Interactive Security Testing & Diagnostics:**
   * Perform reconnaissance against self-owned wireless access points.
   * Evaluate network management frame resilience (802.11w MFP).
   * Harvest PMKID hashes for offline dictionary verification.

---

## 4. Acquisition & Flashing Procedures

There are two primary methods to install ESP32 Marauder:
* **Method A (Web Installer - Recommended & Fastest):** One-click flashing directly from a Chrome/Edge browser using WebSerial.
* **Method B (Manual Binary Download & CLI Flashing):** Downloading the pre-compiled `.bin` files into the `firmware/` directory and flashing via `esptool.py`.

---

### Method A: One-Click Web Installer (Fastest)

1. Connect the ESP32 DevKit V1 to the PC via Micro-USB.
2. Open Google Chrome or Microsoft Edge and navigate to the official Marauder web installer:
   * **URL:** [https://justcallmekoko.github.io/MarauderInstaller/](https://justcallmekoko.github.io/MarauderInstaller/)
3. Select the appropriate hardware target:
   * Choose **"ESP32 (Standard / No Screen)"** or **"ESP32 Dev Board"**.
4. Click **Connect**, select the serial port (`/dev/ttyACM0` or `/dev/ttyUSB0`), and click **Install Marauder**.
5. The web installer automatically flashes the bootloader, partitions, and application binaries without needing manual command execution.

---

### Method B: Manual Binary Download & CLI Flashing

#### 4.1 Prerequisites
Ensure Python and `esptool` are installed, and user permissions allow access to the serial device node:

```bash
# Verify Python serial tool availability
pip install esptool pyserial

# Add user to dialout group (Linux permission for serial devices)
sudo usermod -aG dialout $USER
```

#### 4.2 Downloading Firmware Binaries into `firmware/`
The official firmware binaries are released on the project's GitHub release repository:
* **GitHub Releases:** [https://github.com/justcallmekoko/ESP32Marauder/releases](https://github.com/justcallmekoko/ESP32Marauder/releases)

For the headless ESP32 DevKit V1 (v1.20.0 release), you only need these specific files (no need to download the full repository source code):

1. **Main Application Firmware:**
   * `esp32_marauder_v1_20_0_20261028_esp32_lddb.bin` (under Release Assets)
2. **Bootloader, Partitions & Boot App:**
   *(Click "Show all 33 assets" on the release page or grab from `FlashFiles/`)*
   * `esp32_marauder.ino.bootloader.bin` (or `bootloader.bin`)
   * `esp32_marauder.ino.partitions.bin` (or `partitions.bin`)
   * `boot_app0.bin`

Place these files directly into the `esp32/marauder/firmware/` directory:

```bash
# Verify your downloaded files exist in firmware/:
ls -la esp32/marauder/firmware/
```

#### 4.3 Step 1: Query Chip Information
Verify communication and read MAC address and flash size:

> [!TIP]
> **Serial Port Across Operating Systems:**  
> * **Linux:** `/dev/ttyACM0` or `/dev/ttyUSB0`  
> * **Windows:** `COM3`, `COM4`, etc.  
> * **macOS:** `/dev/cu.usbserial-*` or `/dev/cu.usbmodem*`  
> *(Replace `/dev/ttyACM0` below with your respective OS serial port).*

```bash
esptool.py --port /dev/ttyACM0 chip_id
```

#### 4.4 Step 2: Erase Flash Memory
Erase existing firmware partitions to ensure a clean slate:

```bash
esptool.py --port /dev/ttyACM0 --baud 921600 erase_flash
```
*(If the connection times out, hold down the `BOOT` button on the board while the command initiates).*

#### 4.5 Step 3: Flash the Firmware Binaries
From the `esp32/marauder` directory, flash the binaries to their exact memory offsets:

```bash
cd esp32/marauder

esptool.py --chip esp32 --port /dev/ttyACM0 --baud 921600 write_flash -z \
  0x1000 firmware/esp32_marauder_installer_v1_20_0_20261028_esp32_lddb.bootloader.bin \
  0x8000 firmware/esp32_marauder_installer_v1_20_0_20261028_esp32_lddb.partition-table.bin \
  0xe000 firmware/esp32_marauder_installer_v1_20_0_20261028_esp32_lddb.ota-data.bin \
  0x10000 firmware/esp32_marauder_installer_v1_20_0_20261028_esp32_lddb.bin
```

---

## 5. Serial Interface & CLI Operation

Once flashing is complete, press the **`EN`** button on the ESP32. Open a serial connection at **115200 baud**:

```bash
# Using the project's cross-platform launcher (auto-detects serial port):
python3 scripts/marauder_terminal.py

# Or explicitly pass port:
python3 scripts/marauder_terminal.py /dev/ttyACM0

# Or using picocom / miniterm:
picocom -b 115200 /dev/ttyACM0
# python3 -m serial.tools.miniterm /dev/ttyACM0 115200
```

### Essential Marauder Command Reference

| Command | Function / Objective |
| :--- | :--- |
| `help` | Displays the complete list of available Marauder commands. |
| `scan ap` | Scans and enumerates nearby 2.4 GHz Access Points (SSID, BSSID, RSSI, Channel). |
| `list -a` | Displays the enumerated list of discovered Access Points with assigned index IDs. |
| `select -a <id>` | Selects a specific Access Point index for targeted testing. |
| `sniff pmkid` | Initiates PMKID harvesting against the selected target Access Point. |
| `sniff beacon` | Captures beacon management frames from surrounding networks. |
| `scan station` | Scans for active client stations associated with nearby networks. |
| `stopscan` | Halts any active scanning or sniffing routine. |
| `reboot` | Soft reboots the ESP32 microprocessor. |

---

## 6. Defensive Auditing Applications

1. **802.11w Management Frame Protection (MFP) Testing:**
   * Audit whether modern Access Points drop unauthenticated deauthentication frames.
   * Identifies legacy configuration gaps across enterprise and residential routers.

2. **PMKID Strength Auditing:**
   * Evaluate whether pre-shared keys (WPA2-PSK) are susceptible to dictionary attacks without disrupting connected users.

3. **Rogue AP Detection & Spectrum Reconnaissance:**
   * Identify unauthorized or spoofed Wi-Fi access points emitting overlapping SSIDs.

---

## 7. Ethics & Legal Compliance

> **IMPORTANT NOTICE:**  
> This documentation, firmware, and associated hardware are strictly for **independent educational research, personal self-study, and authorized defensive security assessments** conducted on privately owned networks or authorized lab environments.  
> Intercepting, disrupting, or targeting third-party networks without explicit authorization is strictly illegal under applicable national and international cybercrime legislation.

