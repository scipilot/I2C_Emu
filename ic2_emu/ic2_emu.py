
# Interface to emulate the I2C driver.
# Note most of the settings are ignored (bus, address etc)
#
# Author: Pip Jones
# Based on the INTERFACE of Adafruit_GPIO/I2C.py created by Tony DiCola which is Copyright (c) 2014 Adafruit Industries

import logging
import math
import array

# todo: make a DI interface for the renderer?
from texttable import Texttable

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
            #import asciiBus
            # self._bus = asciiLogBus(busnum)
            self._bus = textTableBus(busnum)
        else:
            # Otherwise use the provided class to create an smbus interface.
            self._bus = i2c_interface(busnum)
        self._logger = logging.getLogger('I2C_Emu.Device.Bus.{0}.Address.{1:#0X}' \
                                .format(busnum, address))

    def writeList(self, register, data):
        """Write bytes to the specified register."""
        self._logger.debug(".writeList:Writing list:%s to register 0x%02X", data, register)
        self._bus.write_i2c_block_data(self._address, register, data)

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        self._logger.debug(".write8:Writing value:0x%02X to register 0x%02X", value, register)
        self._bus.write_byte_data(self._address, register, value)


"""
The rows/columns are represented by register/value combinations.
- R00 = Green pixels in row 1
- R01 = Red pixels in row 1
- R0E = Green pixels in row 8
- R0F = Red pixels in row 8
- Red+Green = Yellow 

The columns are set/cleared by bits in the data: 
- 00 = all off, 
- 01, 02, 04 ... 80 = individual pixels
- FF = all on

Address = 112

The emulator has to update the output display per-pixel change (there is no "frame").
"""

class asciiLogBus(object):
    """
    Writes all output into ASCII
    """

    def __init__(self, busnum):
        self._logger = logging.getLogger('I2C_Emu.asciiLogBus')

    def write_i2c_block_data(self, address, register, data):
        self._logger.debug('write_i2c_block_data({0},{1},{2})' .format(address, register, data))

    def write_byte_data(self, address, register, value):
        self._logger.debug('write_byte_data({0},{1},{2})' .format(address, register, value))

class textTableBus(object):
    """
    Writes all output into ASCII Table on the console
    Using https://github.com/foutaise/texttable/
    """

    def __init__(self, busnum):
        self._logger = logging.getLogger('I2C_Emu.textTableBus')
        # initialise internal data buffer array
        self.data = [[0 for j in range(8)] for i in range(8)]

    def draw(self):
        table = Texttable()
        #table.set_cols_align(["l", "r", "c"])
        #table.set_cols_valign(["t", "m", "b"])
        # Column indexes
        table.add_row(["1", "2", "3", "4", "5", "6", "7", "8"])
        for row in self.data:
            # todo prepend row index?
            table.add_row([self.render_pixel(col) for col in row])
        print(table.draw() + "\n")

    def write_i2c_block_data(self, address, register, data):
        self._logger.debug('write_i2c_block_data({0},{1},{2})' .format(address, register, data))

    def write_byte_data(self, address, register, value):
        """"Sets/Clears a pixel into data buffer array"""
        self._logger.debug('write_byte_data({0},{1},{2})' .format(address, register, value))
        # Odd/even = colour for the bi-colour display
        [row, mod] = divmod(register, 2)
        # colourBit is the pixel colour we're turning on or off in the colour bit mask
        colourBit = 0 if mod else 1
        self._logger.debug('row:{0} colour:{1} ' .format(row, colourBit))

        # Map to array row from bitfield
        for j in range(8):
            # Set this colour's bit in our colour mask
            self.data[row][j] = self.set_bit(self.data[row][j], colourBit, (value & pow(2, j)))
            self._logger.debug('pixel j:{0} set:{2} now:{1:02b} '.format(j, self.data[row][j], (value & pow(2, j))))

        # print("Draw: row:{0} colour:{1} cells:{2:08b}(0x{2:x})".format(row, colourBit, value))
        self.draw()

    def render_pixel(self, value):
        """Decodes the GR=Y combination"""
        return {0: ' ', 1: 'G', 2: 'R', 3: 'Y'}[value]

    def set_bit(self, v, index, x):
        """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
        mask = 1 << index  # Compute mask, an integer with just bit 'index' set.
        v &= ~mask  # Clear the bit indicated by the mask (if x is False)
        if x: v |= mask  # If x was True, set the bit indicated by the mask.
        return v
