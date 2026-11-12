#!/usr/bin/env python3
"""
Simple interactive Serial Terminal launcher for ESP32 Marauder.
Runs at 115200 baud on /dev/ttyACM0.
"""

import sys
import serial
import threading

PORT = '/dev/ttyACM0'
BAUD = 115200

def read_serial(ser):
    while True:
        try:
            line = ser.readline()
            if line:
                sys.stdout.write(line.decode('utf-8', errors='ignore'))
                sys.stdout.flush()
        except Exception:
            break

def main():
    port = sys.argv[1] if len(sys.argv) > 1 else PORT
    print(f"[*] Connecting to ESP32 Marauder on {port} @ {BAUD} baud...")
    print("[*] Press Ctrl+C to exit.\n")
    
    try:
        ser = serial.Serial(port, BAUD, timeout=1)
    except Exception as e:
        print(f"[-] Failed to open serial port {port}: {e}")
        return

    # Start listener thread
    t = threading.Thread(target=read_serial, args=(ser,), daemon=True)
    t.start()

    # Prompt user for commands
    try:
        # Send an initial newline to wake the CLI prompt
        ser.write(b"\r\n")
        while True:
            cmd = input()
            ser.write((cmd + "\r\n").encode('utf-8'))
    except (KeyboardInterrupt, EOFError):
        print("\n[*] Disconnecting...")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
