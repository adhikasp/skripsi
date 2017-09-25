#!/usr/bin/env python
'''
Android client
'''
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import plyer
import logging
import struct


def binary_to_array(num):
    '''
    Convert a number to bit representation in an array
    '''
    # Taken from https://stackoverflow.com/a/16444786/4504053
    binary_string = bin(struct.unpack('!i', struct.pack('!f', num))[0])
    return [True if x == '1' else False for x in binary_string]


if __name__ == '__main__':
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    client = ModbusClient('localhost', port=5020)
    client.connect()

    log.debug('Send gyro data')
    plyer.gyroscope.enable()
    x, y, z = plyer.gyroscope.orientation
    plyer.gyroscope.disable()
    address_offset = 1
    for data in (x, y, z):
        log.debug('Sending value: ' + data)
        binary_data = binary_to_array(data)
        log.debug('Data length: ' + len(binary_data))
        rr = client.write_coils(address_offset, binary_data, unit=0x01)
        address_offset += len(binary_data)

    client.close()
