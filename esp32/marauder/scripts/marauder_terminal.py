#!/usr/bin/env python3
"""
Interactive Serial Terminal launcher for ESP32 Marauder.
Cross-platform: Auto-detects serial ports on Linux, macOS, and Windows.
Runs at 115200 baud.
"""

import sys
import os
import threading
import serial
import serial.tools.list_ports

BAUD_RATE = 115200

def detect_port():
    """Auto-detect available USB serial port or fallback gracefully."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        # Default fallback by OS
        return "COM3" if os.name == 'nt' else "/dev/ttyACM0"
    
    # Priority check for common USB-to-UART identifiers
    for p in ports:
        desc = (p.description or "").lower()
        hwid = (p.hwid or "").lower()
        dev = p.device
        if any(k in desc or k in hwid for k in ["usb", "cp210", "ch34", "serial", "uart", "acm"]):
            return dev
            
    return ports[0].device

def read_serial(ser):
    """Background thread listening for incoming serial stream."""
    while True:
        try:
            line = ser.readline()
            if line:
                sys.stdout.write(line.decode('utf-8', errors='ignore'))
                sys.stdout.flush()
        except Exception:
            break

def main():
    if len(sys.argv) > 1 and sys.argv[1] not in ["-h", "--help"]:
        port = sys.argv[1]
    else:
        if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
            print(f"Usage: {sys.argv[0]} [SERIAL_PORT]")
            print("Example: python3 marauder_terminal.py /dev/ttyUSB0 (or COM3 on Windows)")
            return
        port = detect_port()

    print("==================================================")
    print(f" [*] Target Port : {port}")
    print(f" [*] Baud Rate   : {BAUD_RATE}")
    print(" [*] Controls    : Type Marauder commands & press Enter")
    print(" [*] Exit        : Press Ctrl+C to terminate session")
    print("==================================================\n")

    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
    except Exception as e:
        print(f"[-] Error: Could not connect to {port}: {e}")
        available = [p.device for p in serial.tools.list_ports.comports()]
        if available:
            print(f"[*] Available serial ports detected: {', '.join(available)}")
            print(f"[*] Try running: python3 {sys.argv[0]} <PORT>")
        return

    # Start serial reader thread
    t = threading.Thread(target=read_serial, args=(ser,), daemon=True)
    t.start()

    # CLI interaction loop
    try:
        # Send initial newline to prompt the CLI interface
        ser.write(b"\r\n")
        while True:
            cmd = input()
            ser.write((cmd + "\r\n").encode('utf-8'))
    except (KeyboardInterrupt, EOFError):
        print("\n[*] Disconnecting from Marauder...")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
