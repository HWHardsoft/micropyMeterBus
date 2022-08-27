"""
    Micropython Example Code for MBUS (MKR) shield

    This program will demonstrate the MBUS data request
    via primary and secondary address

    (c) 2022 by Zihatec GmbH - www.zihatec.de

    :copyright: (c) 2017-2019 by Mikael Ganehag Brorsson.
    :license: BSD, see LICENSE for more details.
"""

from machine import UART, Pin
import meterbus.serial
import time
import os
# import stat
import ujson as json


import meterbus

ser = UART(1)

# enable the following lines for Arduino Portenta
# ser.init(2400, bits=8, parity=0, stop=1)
# delay = 0.1

# enable the following lines for Raspberry Pico with RP2040
ser.init(2400, bits=8, parity=0, stop=1,  tx=Pin(4), rx=Pin(5))
delay = 0.5

def ping_address(ser, address, retries=5, read_echo=False):
    for i in range(0, retries + 1):
        meterbus.send_ping_frame(ser, address, read_echo)
        try:
            frame = meterbus.load(meterbus.recv_frame(ser, 1))
            if isinstance(frame, meterbus.TelegramACK):
                return True
        except meterbus.MBusFrameDecodeError as e:
            pass

        time.sleep(0.5)

    return False


def do_char_dev(ser, addr, retries):
    address = None

    try:
        address = int(addr)
        if not (0 <= address <= 254):
            address = addr
    except ValueError:
        address = addr.upper()

    frame = None

    if meterbus.is_primary_address(address):
        ping_address(ser, meterbus.ADDRESS_NETWORK_LAYER, 0)
        time.sleep(delay)
        meterbus.send_request_frame(ser, address)
        time.sleep(delay)
        frame = meterbus.load(
            meterbus.recv_frame(ser, meterbus.FRAME_DATA_LENGTH))


    elif meterbus.is_secondary_address(address):
        meterbus.send_select_frame(ser, address, False)
        time.sleep(delay)
        try:
            frame = meterbus.load(meterbus.recv_frame(ser, 1))
        except meterbus.MBusFrameDecodeError as e:
            frame = e.value

        time.sleep(delay)
        # Ensure that the select frame request was handled by the slave
        assert isinstance(frame, meterbus.TelegramACK)

        frame = None
        meterbus.send_request_frame(ser, meterbus.ADDRESS_NETWORK_LAYER)

        time.sleep(delay)

        frame = meterbus.load(
            meterbus.recv_frame(ser, meterbus.FRAME_DATA_LENGTH))

    else:
        print("no valid address")


    if frame is not None:
        print(frame.to_JSON())



# main
print("Read device with primary address 2 ...")
do_char_dev(ser, 2, 1)


print("Read device with secondary address 2400821196151600 ...")
do_char_dev(ser, "2400821196151600", 1)

