#!/usr/bin/env python
'''
Pymodbus Synchronous Server Example
--------------------------------------------------------------------------

The synchronous server is implemented in pure python without any third
party libraries (unless you need to use the serial protocols which require
pyserial). This is helpful in constrained or old environments where using
twisted just is not feasable. What follows is an examle of its use:
'''
from pymodbus.server.sync import StartTcpServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

DATA_BLOCK_ARRAY = [17] * 100
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, DATA_BLOCK_ARRAY),
    co=ModbusSequentialDataBlock(0, DATA_BLOCK_ARRAY),
    hr=ModbusSequentialDataBlock(0, DATA_BLOCK_ARRAY),
    ir=ModbusSequentialDataBlock(0, DATA_BLOCK_ARRAY))
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName  = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName   = 'Pymodbus Server'
identity.MajorMinorRevision = '1.0'

# Run the server

# Tcp:
StartTcpServer(context, identity=identity, address=("10.72.21.89", 5020))

# Udp:
#StartUdpServer(context, identity=identity, address=("localhost", 502))
