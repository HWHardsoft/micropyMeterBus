"""
    python meterbus for micropython
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A library to decode M-Bus frames with micropython
    
    (c) 2022 by Zihatec GmbH - www.zihatec.de

    :copyright: (c) 2017-2019 by Mikael Ganehag Brorsson.
    :license: BSD, see LICENSE for more details.
"""

# from globals import g
from meterbus.defines import *

from meterbus.core_objects import DataEncoding, FunctionType, MeasureUnit, VIFUnit, \
    VIFUnitExt, VIFUnitSecExt, VIFTable, DateCalculator

from meterbus.telegram_ack import TelegramACK
from meterbus.telegram_short import TelegramShort
from meterbus.telegram_control import TelegramControl
from meterbus.telegram_long import TelegramLong

from meterbus.data_information_block import DataInformationBlock
from meterbus.value_information_block import ValueInformationBlock
from meterbus.telegram_header import TelegramHeader
from meterbus.telegram_body import TelegramBody, TelegramBodyHeader, \
    TelegramBodyPayload
from meterbus.telegram_field import TelegramField
from meterbus.telegram_variable_data_record import TelegramVariableDataRecord

# from wtelegram_snd_nr import WTelegramSndNr
# from wtelegram_body import WTelegramFrame
# from wtelegram_header import WTelegramHeader

from .exceptions import MBusFrameDecodeError, FrameMismatch

from .serial import *
from .auxiliary import *

__author__ = "Mikael Ganehag Brorsson"
__license__ = "BSD-3-Clause"
__version__ = "0.8.1"


def load(data):
    if not data:
        raise MBusFrameDecodeError("empty frame", data)

    if isinstance(data, str):
        data = list(map(ord, data))

    elif isinstance(data, bytes):
        data = list(data)

    elif isinstance(data, bytearray):
        data = list(data)

    elif isinstance(data, list):
        pass

    for Frame in [TelegramACK, TelegramShort, TelegramControl,
                  TelegramLong]:
        try:
            return Frame.parse(data)

        except FrameMismatch as e:
            pass

    raise MBusFrameDecodeError("unable to decode frame")

def debug(state):
  g.debug = state
