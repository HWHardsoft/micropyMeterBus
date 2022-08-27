"""
    Micropython Example Code for MBUS (MKR) shield

    This program will demonstrate the MBUS secondary address scan

    (c) 2022 by Zihatec GmbH - www.zihatec.de

    :copyright: (c) 2017-2019 by Mikael Ganehag Brorsson.
    :license: BSD, see LICENSE for more details.
"""

from machine import UART, Pin
import meterbus.serial
import time
import meterbus

ser = UART(1)

# enable the following lines for Arduino Portenta
# ser.init(2400, bits=8, parity=0, stop=1)
# delay = 0.1

# enable the following lines for Raspberry Pico with RP2040
ser.init(2400, bits=8, parity=0, stop=1,  tx=Pin(4), rx=Pin(5))
delay = 0.5


def ping_address(ser, address, retries=5):
    for i in range(0, retries + 1):
        meterbus.send_ping_frame(ser, address)
        time.sleep(0.2)
        try:
            frame = meterbus.load(meterbus.recv_frame(ser, 1))
            if isinstance(frame, meterbus.TelegramACK):
                return True
        # except:
        except meterbus.MBusFrameDecodeError:
            pass
    return False


def init_slaves(ser):
    if ping_address(ser, meterbus.ADDRESS_NETWORK_LAYER,0) is False:
        return ping_address(ser, meterbus.ADDRESS_BROADCAST_NOREPLY, 0)
    else:
        return True

    return False


def mbus_scan_secondary_address_range(ser, pos, mask, read_echo=False):
    # F character is a wildcard
    if mask[pos].upper() == "F":
        l_start, l_end = 0, 9
    else:
        if pos < 15:
            mbus_scan_secondary_address_range(ser, pos + 1, mask)
        else:
            l_start = l_end = ord(mask[pos]) - ord("0")

    time.sleep(1)
    if mask[pos].upper() == "F" or pos == 15:
        for i in range(l_start, l_end + 1):  # l_end+1 is to include l_end val
            new_mask = (mask[:pos] + "{0:1X}".format(i) + mask[pos + 1 :]).upper()
            val, match, manufacturer = mbus_probe_secondary_address(
                ser, new_mask
            )
            if val is True:
                print(
                    "Device found with id {0} ({1}), using mask {2}".format(
                        match, manufacturer, new_mask
                    )
                )
            elif val is False:  # Collision
                mbus_scan_secondary_address_range(ser, pos + 1, new_mask)


def mbus_probe_secondary_address(ser, mask, read_echo=False):
    # False -> Collison
    # None -> No reply
    # True -> Single reply
    meterbus.send_select_frame(ser, mask)
    time.sleep(delay)
    try:
        frame = meterbus.load(meterbus.recv_frame(ser, 1))
    except meterbus.MBusFrameDecodeError as e:
        frame = e.value


    if isinstance(frame, meterbus.TelegramACK):
        meterbus.send_request_frame(
            ser, meterbus.ADDRESS_NETWORK_LAYER)
        time.sleep(delay)

        frame = None
        try:
            frame = meterbus.load(meterbus.recv_frame(ser))
        except meterbus.MBusFrameDecodeError:
            pass

        if isinstance(frame, meterbus.TelegramLong):
            return True, frame.secondary_address, frame.manufacturer

        return None, None, None

    return frame, None, None

# main routine
# Ensure we are at the beginning of the records
print("Init slaves...")
init_slaves(ser)

# Start scanning for secondary addresses
print("Scan M-Bus for slaves with secondary address - mask FFFFFFFFFFFFFFFF ...")
mbus_scan_secondary_address_range(ser, 0, "FFFFFFFFFFFFFFFF", False)





