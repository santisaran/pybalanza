#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
"""
Handling raw data inputs example
"""
from time import sleep
from pywinusb import hid

def sample_handler(data):
    global contador
    if contador == 1:
        contador = 0
        #~ print "Peso: ", 
        #~ peso = int(chr(data[1]))*1000 + int(chr(data[2]))*100 + int(chr(data[3]))*10 +int(chr(data[4]))
        #~ print peso
        print data[1]
    contador+=1

def raw_test():
    global contador
    filtro = hid.HidDeviceFilter(vendor_id=0x1345,product_id=0x1000)
    balanza = filtro.get_devices()[0]
    contador=0
    try:
        balanza.open()
        balanza.set_raw_data_handler(sample_handler)
        while balanza.is_plugged():
            sleep(2)
        print "puerto desenchufado"
        return
    finally:
        balanza.close()
#
if __name__ == '__main__':
    raw_test()
    print contador

