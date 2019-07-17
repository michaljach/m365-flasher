# ```m365 Firmware Flasher BLE 🚀```
Python script to flash your Xiomi Mija Scooter Firmware via BLE (Bluetooth Low Energy). It uses Core Bluetooth Framework on OS X and works natively to OS.

### Requirements
- Pyhton 2.7
- macOS 10.10+
- BLE compatible device (Bluetooth 5.0)

### Usage
```
python ble.py firmware.bin
```

### API

```
positional arguments:
  file        firmware file

optional arguments:
  -h, --help  show this help message and exit

Example:  ble.py firmware.bin - flash firmware.bin to ESC using BLE protocol
```
