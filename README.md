# ```m365 Firmware Flasher BLE 🚀```
Python script to flash your Xiaomi Mijia 365 Scooter Firmware via BLE (Bluetooth Low Energy). It uses Core Bluetooth Framework on OS X and works natively to OS.

### Requirements
- Pyhton 2.7
- macOS 10.10+
- BLE compatible device (Bluetooth 5.0)

### Usage
```
python ble.py 68753A44-4D6F-1226-9C60-0050E4C00067 firmware.bin
```

### API

```
positional arguments:
  device      scooter UUID
  file        firmware file

optional arguments:
  -h, --help  show this help message and exit

Example:  ble.py 68753A44-4D6F-1226-9C60-0050E4C00067 firmware.bin - flash firmware.bin to ESC using BLE protocol
```
