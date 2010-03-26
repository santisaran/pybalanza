#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Read inputs from an HID device

# Select the device
import socket
try:
    n = 0
    f = open('/dev/hidraw1', 'r')
    length = 32
    s = socket.socket()
    s.connect(("localhost", 9999))
    
    while True:
        input = f.read(length)
       
        n+=1
        #if n>5:
        s.send(input)
        print input+"\r",
        n = 0;
            
except KeyboardInterrupt:
    s.send("quit")
    f.close()
    s.close()
    print "detención por teclado"

