# Cybersecurity Research & Ethical Hacking Toolkit

An open-source, modular repository dedicated to educational cybersecurity research, ethical hacking experiments, hardware security analysis, and defensive network auditing.

---

## 📌 Project Overview

This repository serves as a centralized hub for ongoing hands-on cybersecurity research and laboratory experiments. Designed to expand over time, it encompasses diverse areas of offensive security principles, defensive validation, hardware micro-controller testing, and custom security scripts.

All materials, scripts, and documentation within this project are developed as part of independent personal research, self-study, and authorized laboratory simulations.

---

## 📂 Repository Structure

The project is structured modularly to support multiple domains of security exploration:

```text
├── esp32/                        # Hardware Hacking & Wireless Auditing
│   ├── docs/
│   │   └── esp32_overview_and_capabilities.md   # ESP32 DevKit V1 Hardware & Wi-Fi Guide
│   └── marauder/                 # ESP32 Marauder Wireless Auditing Suite
│       ├── docs/
│       │   ├── workflow_and_flashing_guide.md   # Flashing & Deployment Guide
│       │   └── hands_on_lab_guide.md            # Step-by-Step Hands-On Labs Manual
│       ├── firmware/                            # Pre-compiled Marauder binaries
│       └── scripts/
│           └── marauder_terminal.py             # Cross-platform interactive serial terminal
├── network-auditing/             # (Planned) Packet analysis, port scanning, traffic monitors
├── web-security/                 # (Planned) Security test beds, API audits, validation scripts
├── cryptography-labs/            # (Planned) Hash cracking benchmarks, cipher analyses
├── scripts/                      # (Planned) Multi-purpose Python, Bash, and automation utilities
├── .gitignore                    # Prevents commits of sensitive logs, pcaps, and build artifacts
├── LICENSE                       # Open-Source License
└── README.md                     # Main project guide
```

---

## 🔬 Current Modules

### 1. Embedded & Hardware Security (`esp32/`)
* **Hardware Target:** ESP32 DevKit V1 (ESP-WROOM-32).
* **Research Focus:** 
  * Wi-Fi 802.11 Promiscuous Mode frame inspection.
  * EAPOL handshake & PMKID capture for offline password audit experiments.
  * Testing 802.11w Management Frame Protection (MFP) resilience.
  * Bluetooth Low Energy (BLE) advertisement scanning and IoT perimeter assessment.
* **Core Documentation & Guides:**
  * [esp32_overview_and_capabilities.md](esp32/docs/esp32_overview_and_capabilities.md): Hardware architectural breakdown.
  * [workflow_and_flashing_guide.md](esp32/marauder/docs/workflow_and_flashing_guide.md): Complete flashing and deployment procedure.
  * [hands_on_lab_guide.md](esp32/marauder/docs/hands_on_lab_guide.md): Practical step-by-step wireless security lab manual.

---

## 🗺️ Roadmap & Upcoming Additions

- [x] Hardware architecture & wireless capability documentation (ESP32).
- [ ] ESP32 raw packet capture (`.pcap`) streaming to Wireshark via serial/web.
- [ ] Custom Python network scanning & diagnostic scripts.
- [ ] Password complexity testing workflows using hash auditing utilities.
- [ ] Rogue Access Point & Captive Portal simulation templates for awareness training.
- [ ] BLE device mapping and RSSI localization tools.

---

## 🛡️ Ethics, Legal Compliance & Disclaimer

> **DISCLAIMER:**  
> The contents of this repository are provided exclusively for **independent educational, self-study, and defensive research purposes**. 
> All experiments and tools must be executed only on hardware, networks, and systems that you own or have explicit, documented authorization to test. 
> The author and contributors assume no liability for misuse or damage caused by the application of techniques documented here.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

