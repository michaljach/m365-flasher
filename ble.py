#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import sys
import os
import argparse
import time

from binascii import hexlify
from struct import pack, unpack
from Foundation import *
from PyObjCTools import AppHelper

class BleClass(object):

    def centralManagerDidUpdateState_(self, manager):
        self.manager = manager
        manager.scanForPeripheralsWithServices_options_(None,None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        self.peripheral = peripheral
        if args.device in repr(peripheral.UUID):
            print 'DeviceName: ' + peripheral.name()
            manager.connectPeripheral_options_(peripheral, None)
            manager.stopScan()

    def centralManager_didConnectPeripheral_(self, manager, peripheral):
        peripheral.setDelegate_(self)
        self.peripheral.discoverServices_([])
        
    def peripheral_didDiscoverServices_(self, peripheral, services):
        self.service = self.peripheral.services()[0]
        self.peripheral.discoverCharacteristics_forService_([], self.service)

    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
      write = self.service.characteristics()[1]
    
      for characteristic in self.service.characteristics():
        if characteristic.UUID() == write.UUID():
            self.characteristic = characteristic
            self.UpdateFirmware(args.file)

    def peripheral_didReceiveReadRequest_error_(self, peripheral, characteristic, error):
      print 'Read ERR'

    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print 'ERROR:' + repr(error)
        if self.characteristic.UUID() == characteristic.UUID():
            print("Cool")

    def sendMessage(self, packet):
        byte = NSData.dataWithBytes_length_(packet, len(packet))
        # self.peripheral.writeValue_forCharacteristic_type_(byte, self.characteristic, 0)

    def createPacket(self, address, cmd, arg, payload):
        packet = pack("<BBBB", len(payload)+2, address, cmd, arg) + payload
        return "\x55\xAA" + packet + pack("<H", self.checksum(packet))

    def checksum(self, data, s = 0):
        s = 0
        for c in data:
            s += ord(c)
        return (s & 0xFFFF) ^ 0xFFFF
    
    def UpdateFirmware(self, fwfile):
        fwfile.seek(0, os.SEEK_END)
        fw_size = fwfile.tell()
        fwfile.seek(0)
        fw_page_size = 0x80

        print('Ready')

        print('Locking...')
        packet = self.createPacket(0x20, 0x03, 0x70, pack("<H", 0x0001))
        print '>', hexlify(packet).upper()
        self.sendMessage(packet)
        time.sleep(1)
        
        print('Starting...')
        packet = self.createPacket(0x20, 0x07, 0x00, pack("<L", fw_size))
        print '>', hexlify(packet).upper()
        self.sendMessage(packet)
        time.sleep(1)

        print('Writing...')
        page = 0
        chk = 0
        while fw_size:
            chunk_sz = min(fw_size, fw_page_size)
            read = fwfile.read(chunk_sz)
            chk = self.checksum(read, chk)
            data = read+b'\x00'*(fw_page_size-chunk_sz)
            packet = self.createPacket(0x20, 0x08, page, data)
            print '>', hexlify(packet).upper()
            self.sendMessage(packet)
            time.sleep(0.3)
            page += 1
            fw_size -= chunk_sz

        print('Finalizing...')
        data = pack("<L", chk ^ 0xFFFFFFFF)
        packet = self.createPacket(0x20, 0x09, 0x00, data)
        print '>', hexlify(packet).upper()
        self.sendMessage(packet)
        time.sleep(1)

        print('Reboot')
        data = pack("<H", 0x00)
        packet = self.createPacket(0x20, 0x0A, 0x00, data)
        print '>', hexlify(packet).upper()
        self.sendMessage(packet)

        print('Done')
        return True

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
	description='Xiaomi m365 firmware flasher',
	epilog='Example:  %(prog)s 68753A44-4D6F-1226-9C60-0050E4C00067 firmware.bin - flash firmware.bin to ESC using BLE protocol')

parser.add_argument('device', type=str.upper, help='scooter UUID')
parser.add_argument('file', type=argparse.FileType('rb'), help='firmware file')

args = parser.parse_args()

if "__main__" == __name__:
  try:
    central_manager = CBCentralManager.alloc()
    central_manager.initWithDelegate_queue_options_(BleClass(), None, None)
    AppHelper.runConsoleEventLoop()
  except KeyboardInterrupt:
    sys.exit()