"""
    Micropython Example Code for MBUS (MKR) shield

    This program will demonstrate the MBUS primary (logical) address scan

    (c) 2022 by Zihatec GmbH - www.zihatec.de

    :copyright: (c) 2017-2019 by Mikael Ganehag Brorsson.
    :license: BSD, see LICENSE for more details.
"""

from machine import UART, Pin
import meterbus.serial
import time
import meterbus


ser = UART(1)

# enable the following line for Arduino Portenta
# ser.init(2400, bits=8, parity=0, stop=1)

# enable the following line for Raspberry Pico with RP2040
ser.init(2400, bits=8, parity=0, stop=1,  tx=Pin(4), rx=Pin(5))
 

def ping_address(address, retries=5):
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

# main routine
print("Start MBUS Scan...")
for address in range(0, meterbus.MAX_PRIMARY_SLAVES + 1):
    time.sleep(1)
    print("Scan Address:" + str(address), end="" )
    if ping_address(address, 3):
        print(" Found M-Bus device!!!")
    else:
        print(" no device found")
