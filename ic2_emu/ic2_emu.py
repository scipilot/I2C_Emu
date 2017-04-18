
# Interface to emulate the I2C driver.
# Note most of the settings are ignored (bus, address etc)
#
# Author: Pip Jones
# Based on the INTERFACE of Adafruit_GPIO/I2C.py created by Tony DiCola which is Copyright (c) 2014 Adafruit Industries

import logging

def get_i2c_device(address, busnum=None, i2c_interface=None, **kwargs):
    """Return an I2C device for the specified address and on the specified bus.
    If busnum isn't specified, the default I2C bus for the platform will attempt
    to be detected.
    """
    if busnum is None:
        busnum = 0
    return Device(address, busnum, i2c_interface, **kwargs)


class Device(object):
    """Class for communicating with an I2C device using the adafruit-pureio pure
    python smbus library, or other smbus compatible I2C interface. Allows reading
    and writing 8-bit, 16-bit, and byte array values to registers
    on the device."""
    def __init__(self, address, busnum, i2c_interface=None):
        """Create an instance of the I2C device at the specified address on the
        specified I2C bus number."""
        self._address = address
        if i2c_interface is None:
            # Use pure python I2C interface if none is specified.
            import IC2_Emu.asciiBus
            self._bus = IC2_Emu.asciiBus(busnum)
        else:
            # Otherwise use the provided class to create an smbus interface.
            self._bus = i2c_interface(busnum)
        self._logger = logging.getLogger('I2C_Emu.Device.Bus.{0}.Address.{1:#0X}' \
                                .format(busnum, address))

    def writeList(self, register, data):
        """Write bytes to the specified register."""
        self._bus.write_i2c_block_data(self._address, register, data)
        self._logger.debug("Wrote to register 0x%02X: %s",
                     register, data)

class asciiBus(object):
    """
    Writes all output into ASCII
    """

    def __init__(self, busnum):
        self._logger = logging.getLogger('I2C_Emu.AsciiBus')

    def write_i2c_block_data(self, address, register, data):
        self._logger.debug(self, 'write_i2c_block_data({0},{1},{2})' .format(address, register, data))
