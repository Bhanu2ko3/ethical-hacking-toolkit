# ESP32 Marauder Suite (CLI Edition)

This directory contains resources, binaries, and documentation for deploying the **ESP32 Marauder** wireless security auditing suite on the ESP32 DevKit V1 in headless (CLI) mode.

---

## Directory Organization

* **`docs/`**: Detailed technical guides, memory layouts, and workflow architecture.
  * [workflow_and_flashing_guide.md](docs/workflow_and_flashing_guide.md): Complete flashing and command reference guide.
* **`firmware/`**: Firmware binary packages (`bootloader.bin`, `partitions.bin`, and application binary).
* **`scripts/`**: (Optional) Automation scripts for flashing and serial monitoring.

---

## Quick Reference

* **Target Device:** ESP32 DevKit V1 (ESP-WROOM-32)
* **Serial Port:** `/dev/ttyACM0` (or `/dev/ttyUSB0`)
* **Default Baud Rate:** `115200`
* **Firmware Source:** [JustCallMeKoko / ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder)

