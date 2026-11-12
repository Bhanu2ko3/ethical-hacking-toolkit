# ESP32 DevKit V1 - Hardware Overview & Wireless Security Auditing Guide

## 1. Hardware Overview 

* **Board Model:** ESP32 DevKit V1
* **Module:** ESP-WROOM-32
* **Processor:** Dual-Core Xtensa 32-bit LX6 Microprocessor (up to 240 MHz)
* **Wireless Connectivity:** 2.4 GHz Wi-Fi (802.11 b/g/n), Bluetooth v4.2 & BLE (Bluetooth Low Energy)
* **Memory:** 520 KB SRAM, 4 MB On-board Flash Memory
* **Interface & Power:** Micro-USB Port (CP2102/CH340 USB-to-UART Bridge), 30-pin DIP Layout, EN & BOOT Buttons
* **Operating Voltage:** 3.3V Logic / 5V USB Input

---

## 2. Wireless Security Auditing Capabilities (Ethical Hacking Applications)

### 2.1 Wi-Fi Packet Sniffing & Monitoring
* **Theoretical Mechanism:** Uses ESP32's **802.11 Promiscuous Mode** to inspect raw MAC-level IEEE 802.11 frames without connecting or authenticating to an Access Point.
* **Educational & Defensive Use:**
  * Detecting Hidden SSIDs.
  * Inspecting surrounding Access Points and active clients (MAC addresses & RSSI signal strength).
  * Capturing raw Wi-Fi traffic into `.pcap` files for deep analysis in Wireshark.

### 2.2 WPA2 PMKID & Handshake Capture
* **Theoretical Mechanism:** Captures the **Pairwise Master Key Identifier (PMKID)** embedded in RSN Information Elements during EAPOL 4-Way Handshakes.
* **Educational & Defensive Use:**
  * Offline WPA2-PSK password complexity auditing.
  * Exporting captured hashes to tools like **Hashcat** or **John the Ripper** to test password strength against dictionary attacks in lab environments.

### 2.3 802.11 Deauthentication Vulnerability Testing
* **Theoretical Mechanism:** Transmits unauthenticated 802.11 Management Frames (Deauth/Disassociation) to test frame validation.
* **Educational & Defensive Use:**
  * Auditing whether an Access Point has **802.11w (Management Frame Protection - MFP)** or **WPA3** enabled.
  * Demonstrating why unencrypted 802.11 management frames pose security risks on older legacy Wi-Fi hardware.

### 2.4 Rogue Access Point & Captive Portal Demonstrations
* **Theoretical Mechanism:** Configures the ESP32 in **SoftAP (Access Point)** mode running a lightweight embedded HTTP Web Server.
* **Educational & Defensive Use:**
  * Simulating Evil Twin / Rogue AP scenarios for Social Engineering awareness.
  * Demonstrating how open Wi-Fi captive portals can be spoofed, highlighting the importance of HTTPS and VPNs.

### 2.5 Beacon Flooding & Stress Testing
* **Theoretical Mechanism:** Transmits multiple synthetic 802.11 Beacon Management Frames containing arbitrary SSIDs.
* **Educational & Defensive Use:**
  * Testing the resilience and buffer handling of Wi-Fi scanners and Access Point management software under packet load.

### 2.6 Bluetooth Low Energy (BLE) Auditing
* **Theoretical Mechanism:** Uses the internal BLE radio to scan, filter, and transmit BLE advertisements.
* **Educational & Defensive Use:**
  * Auditing IoT device advertisements and BLE beacon security configurations.

---

## 3. Technical Working Principles

1. **Promiscuous Mode (`esp_wifi_set_promiscuous`):** Standard Wi-Fi chips ignore packets not addressed to their MAC. Promiscuous mode instructs the ESP32 MAC layer to pass all received 802.11 frames directly to the application layer.
2. **Raw Frame Transmission (`esp_wifi_80211_tx`):** Allows low-level transmission of custom-constructed 802.11 frames directly onto specified 2.4 GHz channels.

---

## 4. Device Limitations

* **Frequency:** 2.4 GHz band only (No 5 GHz / 6 GHz support).
* **Processing & Memory:** Limited SRAM prevents hosting large full-packet captures or running complex packet processing tools directly on the chip (requires offloading to a host PC).

---

## 5. Popular Open-Source Educational Firmware

* **ESP32 Marauder** (by *JustCallMeKoko*): A comprehensive suite for Wi-Fi & BLE security research.
* **ESP8266 / ESP32 Deauther** (by *Spacehuhn*): An educational tool focused on 802.11 management frame analysis.

---

## 6. Ethics & Legal Notice

> **IMPORTANT:** This documentation and associated hardware are strictly for independent personal research, self-study, and authorized testing on self-owned networks and lab environments. Unauthorized interception or disruption of third-party wireless networks is strictly illegal under cybercrime laws.
