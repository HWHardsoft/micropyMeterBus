# Meter-Bus for MicroPython
MicroPython  implementation of the Meter-Bus (M-Bus EN13757-3) protocol. 

## about M-BUS
Due to rising prices for oil, gas and heat as well as climate change, it is becoming more and more important to monitor energy consumption in order to keep an eye on energy costs, but also to be able to check the effectiveness of savings. Many meters for oil and gas, but also for water, are equipped with a special 2 wire bus system, the [M-BUS or meter bus](https://m-bus.com/), for monitoring consumption values.

## Hardware
I've tested this code with our [Arduino MKR M-BUS shield](https://www.hwhardsoft.de/english/projects/m-bus-mkr-shield/) and the Arduino Portenta H7 (via  OpenMV IDE) and the Raspberry Pico (via Thonny IDE).



![My image](https://user-images.githubusercontent.com/3049858/72681999-3a597480-3ac9-11ea-857b-fae4e47f3a2b.jpg)


## External libraries
MicroPython will not support the decimal function of standard Python. To solve this problem the library [micropython-decimal-number](https://github.com/mpy-dev/micropython-decimal-number) is required.

## Examples
Please enable/ disable the lines for UART configuration in the examples for your board first!

### mbus-serial-scan.py
This program will scan the M-Bus for dievices via the logical address. Currently it is limited to address 6 as maximum, but you can change the  





## Credits
Based on the pyMeterBus project by Mikael Ganehag Brorsson

https://github.com/ganehag/pyMeterBus

