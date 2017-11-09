#!/usr/bin/env python
'''
Android client
'''
from pyModbusTCP.client import ModbusClient
# import plyer
import logging
import struct


def number_to_array_bits(num):
    '''
    Convert a number to bit representation in array format.

    >>> number_to_array_bits(1.0)
    [False, False, True, True, True, True, True, True, True, False, False,
    False, False, False, False, False, False, False, False, False, False,
    False, False, False, False, False, False, False, False, False, False,
    False]
    '''
    # Taken from https://stackoverflow.com/a/16444786/4504053
    binary_string = bin(struct.unpack('!i', struct.pack('!f', num))[0])
    return [True if x == '1' else False for x in binary_string]


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    SERVER_HOST = '10.72.21.89'
    SERVER_PORT = 5020
    logging.debug('Open connection to {}:{}'.format(SERVER_HOST, SERVER_PORT))
    client = ModbusClient(host=SERVER_HOST, port=SERVER_PORT, auto_open=True)

    logging.debug('Send gyro data')
    # plyer.gyroscope.enable()
    # x, y, z = plyer.gyroscope.orientation
    # plyer.gyroscope.disable()
    x, y, z = 1, 0.1, -0.1
    address_offset = 1
    for data in (x, y, z):
        logging.debug('Sending value: {}'.format(data))
        binary_data = number_to_array_bits(data)
        logging.debug('Data length: {}'.format(len(binary_data)))
        rr = client.write_multiple_registers(address_offset, binary_data)
        address_offset += len(binary_data)

    bits = client.read_coils(1, 32)
    logging.debug('Reading data from slave: {}'.format(bits))

    logging.debug('Script complete.')
