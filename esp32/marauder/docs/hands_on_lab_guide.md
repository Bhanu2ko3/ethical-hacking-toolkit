# ESP32 Marauder - Hands-On Wireless Security Lab Manual

A step-by-step educational laboratory curriculum for mastering wireless security auditing, 802.11 protocol analysis, and BLE security using the **ESP32 Marauder (Headless CLI)**.

---

## 🎯 Curriculum Overview

Each laboratory exercise is structured into four core learning pillars:
1. **Underlying Theory:** Low-level 802.11 / BLE protocol mechanics.
2. **Execution Steps:** Exact commands and terminal workflows.
3. **Data Interpretation:** Understanding MAC addresses, RSSI, frame subtypes, and encryption modes.
4. **Defensive Countermeasures:** How network engineers secure and monitor against each vector.

```text
Lab 1: Wireless Reconnaissance & Frame Sniffing
  ├── 802.11 Management frames (Beacons, Probes)
  ├── Discovering Hidden SSIDs
  └── Mapping Access Points and Active Client Stations

Lab 2: WPA2 PMKID & Handshake Harvesting
  ├── 4-Way EAPOL Handshake mechanics
  ├── RSN Information Element PMKID derivation
  └── Exporting hashes for offline password strength auditing

Lab 3: 802.11 Management Frame Protection (MFP / 802.11w) Testing
  ├── Legacy 802.11 unauthenticated management frame flaws
  ├── Executing controlled deauthentication tests
  └── Verifying 802.11w / WPA3 Protected Management Frames

Lab 4: Beacon Flooding & Wireless Stress Testing
  ├── Synthetic beacon frame injection
  ├── Buffer handling and scanner resilience
  └── Defense against rogue SSID spamming

Lab 5: Bluetooth Low Energy (BLE) Auditing
  ├── BLE advertisement packets & Manufacturer Data
  ├── Tracking AirTags and BLE beacons
  └── Evaluating device resilience against BLE pairing spam
```

---

## 🧪 Lab 1: Wireless Reconnaissance & Passive Sniffing

### 1.1 Objective
Capture and enumerate surrounding 2.4 GHz wireless networks without transmitting any probe requests or connecting to an Access Point (Zero-footprint passive discovery).

### 1.2 Protocol Background
* Access Points periodically broadcast **802.11 Beacon Frames** (typically every 102.4 ms / 100 TU) to announce their presence, SSID, supported data rates, and encryption capabilities (WPA2, WPA3).
* When a network is "Hidden", the SSID field in the beacon frame is left empty (length = 0) or filled with null bytes. However, when a client device connects to a hidden network, it sends a **Probe Request / Association Request** containing the actual SSID, which the ESP32 sniffs to unmask the hidden network.

### 1.3 Step-by-Step Execution
Open the Marauder terminal:
```bash
python3 /home/codebro/self-study/hacking-tools/esp32/marauder/scripts/marauder_terminal.py
```

Run the following commands sequentially:
```text
> scanall
```
*(Allow the scanner to hop across channels 1 to 14 for approximately 15 to 20 seconds)*

```text
> stopscan
```

Display discovered Access Points:
```text
> list -a
```

Display discovered Client Stations (connected phones, laptops):
```text
> list -c
```

### 1.4 How to Read the Output
* **Index:** The unique numeric ID assigned to the target for subsequent commands.
* **SSID:** The human-readable wireless network name.
* **BSSID:** The hardware MAC address of the Access Point radio.
* **Ch (Channel):** The 2.4 GHz operating channel (1-14).
* **RSSI:** Received Signal Strength Indicator (in dBm):
  * `-30 to -50 dBm`: Very close / Excellent signal.
  * `-60 to -75 dBm`: Medium / Typical indoor range.
  * `-80 to -90 dBm`: Very weak / Edge of reception.
* **Security:** WEP (Legacy/Broken), WPA, WPA2-PSK, WPA3-SAE, or OPEN.

### 1.5 Defensive Remediation
* Disable legacy WEP and WPA1.
* Recognize that hiding an SSID does **not** provide security; it is easily uncovered through passive traffic sniffing.
* Segment sensitive IoT hardware from primary networks.

---

## 🧪 Lab 2: WPA2 PMKID & Handshake Harvesting

### 2.1 Objective
Capture the **Pairwise Master Key Identifier (PMKID)** from an Access Point's First EAPOL message without disconnecting or waiting for active users.

### 2.2 Protocol Background
In 2018, the Hashcat team discovered that the WPA2 4-Way Handshake protocol embeds a PMKID inside the RSN (Robust Security Network) Information Element of Frame 1:
$$\text{PMKID} = \text{HMAC-SHA1-128}(\text{PMK}, \text{"PMK Name"} \parallel \text{MAC}_{\text{AP}} \parallel \text{MAC}_{\text{STA}})$$
Because this is derived directly from the AP's Pre-Shared Key (PSK), capturing this single packet allows offline dictionary password auditing.

### 2.3 Execution
```text
> list -a
> select -a <target_index>
> sniffpmkid
```
*(Leave running for 1-2 minutes until PMKID packet is captured)*
```text
> stopscan
```

### 2.4 Defensive Remediation
* Implement strong, complex Pre-Shared Keys (> 14 characters, mixed alphanumeric and symbols).
* Transition to **WPA3-Personal (SAE - Simultaneous Authentication of Equals)**, which is inherently immune to offline dictionary attacks.

---

## 🧪 Lab 3: 802.11 Management Frame Resilience (Deauth Audit)

### 3.1 Objective
Evaluate whether a wireless Access Point drops or processes unauthenticated 802.11 Deauthentication management frames.

### 3.2 Protocol Background
Legacy 802.11 standards do not encrypt or digitally sign management frames. An attacker can craft a frame with subtype `0x000C` (Deauthentication) and spoof the AP's source MAC address, causing clients to disconnect immediately.

**The Fix:** **IEEE 802.11w (Management Frame Protection - MFP)** adds a cryptographic Message Integrity Code (BIP - Broadcast Integrity Protocol) to management frames, rendering spoofed deauth frames invalid and ignored.

### 3.3 Execution (Only on self-owned lab networks)
```text
> select -a <self_owned_ap_index>
> attack -t deauth
```
*(Observe client device connection behavior)*
```text
> stopscan
```

### 3.4 Defensive Verification
* Inspect router management console: Ensure **802.11w / MFP** is set to **"Required"** or **"Capable"**.
* Enforce **WPA3**, where 802.11w is mandatory by specification.

---

## 🧪 Lab 4: SSID Beacon Flooding & Buffer Stress Testing

### 4.1 Objective
Assess how client wireless drivers and spectrum scanning tools handle large bursts of synthetic beacon frames.

### 4.2 Protocol Background
Access Points broadcast beacon frames containing network metadata. Generating dozens of synthetic beacons with pseudo-random BSSIDs tests device buffer limits and demonstrates how attackers clutter wireless environments.

### 4.3 Execution
```text
> ssid -a -g 10
> attack -t beacon -a
```
*(Check phone / laptop Wi-Fi picker to observe synthetic networks)*
```text
> stopscan
```

---

## 🧪 Lab 5: Bluetooth Low Energy (BLE) Auditing

### 5.1 Objective
Audit 2.4 GHz BLE advertising channels (37, 38, 39) to detect nearby BLE beacons, Apple AirTags, and test device notification resilience.

### 5.2 Execution
```text
> sniffbt airtag
```
*(Sniffs nearby Apple FindMy / AirTag signals)*
```text
> stopscan
```

Test BLE notification handling:
```text
> blespam -t samsung
```
*(Or `-t windows` / `-t all`)*
```text
> stopscan
```
