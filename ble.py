#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import sys
from Foundation import *
from PyObjCTools import AppHelper

class BleClass(object):

    def centralManagerDidUpdateState_(self, manager):
        self.manager = manager
        manager.scanForPeripheralsWithServices_options_(None,None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        print repr(peripheral.UUID())
        print peripheral.name()
        self.peripheral = peripheral
        if '90D274B0-9F0F-47C6-B72C-63853B856674' in repr(peripheral.UUID):
            print 'DeviceName: ' + peripheral.name()
            manager.connectPeripheral_options_(peripheral, None)
            manager.stopScan()


    def centralManager_didConnectPeripheral_(self, manager, peripheral):
        print repr(peripheral.UUID())
        peripheral.setDelegate_(self)
        self.peripheral.discoverServices_([])
        
    def peripheral_didDiscoverServices_(self, peripheral, services):
        print self.peripheral.services()
        self.service = self.peripheral.services()[1]
        self.peripheral.discoverCharacteristics_forService_([], self.service)

    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
      peripheral.readValueForCharacteristic_(self.service.characteristics()[4])
      for characteristic in self.service.characteristics():
        peripheral.setNotifyValue_(true, characteristic)

    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print 'In error handler'
        print 'ERROR:' + repr(error)

    def peripheral_didUpdateNotificationStateForCharacteristic_error_(self, peripheral, characteristic, error):
        print "Notification handler"
    
    def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
      print characteristic.properties
      print characteristic.value().bytes().tobytes()
        # print repr(characteristic.value().bytes().tobytes())
      value = characteristic.value()

      for test in value:
        print struct.unpack('<B', test)[0]
          
      temp = decode_value(value[1:3])
      print 'data:' + str(temp)

      humid = decode_value(value[3:5],0.01)
      print 'humidity:' + str(humid)

      lum = decode_value(value[5:7])
      print 'lumix:' + str(lum)

      uvi = decode_value(value[9:7], 0.01)
      print 'UV index:' + str(uvi)

      atom = decode_value(value[9:11], 0.1)
      print 'Atom:' + str(atom)

      noise = decode_value(value[11:13], 0.01)
      print 'Noise:' + str(noise)

      disco = decode_value(value[13:15], 0.01)
      print 'Disco:' + str(disco)

      heat = decode_value(value[15:17], 0.01)
      print 'Heat:' + str(heat)
      
      batt = decode_value(value[17:19],0.001)
      print 'Battery:' + str(batt)


# Decoding sensor value from Wx2Beancon Data format.
def decode_value(value, multi=1.0):
    if(len(value) != 2):
        return None
    lsb,msb = struct.unpack('BB',value)
    result = ((msb << 8) + lsb) * multi
    return result

if "__main__" == __name__:
  try:
    # DO THINGS
    central_manager = CBCentralManager.alloc()
    central_manager.initWithDelegate_queue_options_(BleClass(), None, None)
    AppHelper.runConsoleEventLoop()
  except KeyboardInterrupt:
    # quit
    sys.exit()