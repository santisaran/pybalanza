#!/usr/bin/env python
# -*- coding: utf-8 -*-

import usb
import os
import sys
import time
import types
 
class Printer:
 
    '''
    Clase que maneja directamente el puerto USB, preguntando al hardware conectado
    los parametros indicativos del mismo.
    '''
 
    def __init__(self, device, configuration, interface):
 
        if PRINTER_CLASS != interface.interfaceClass:
            raise TypeError, "Tipo de interface non valido!"
 
        self.__devhandle = device.open()
        self.__devhandle.setConfiguration(configuration)
        self.__devhandle.claimInterface(interface)
        self.__devhandle.setAltInterface(interface)
 
        self.__intf = interface.interfaceNumber
        self.__alt    = interface.alternateSetting
 
        self.__conf = (type(configuration) == types.IntType \
                        or type(configuration) == types.LongType) and \
                        configuration or \
                        configuration.value
 
        self.__bulkout    = 1
        self.__bulkin     = 0x82
 
    def __del__(self):
 
        try:
            self.__devhandle.releaseInterface(self.__intf)
            del self.__devhandle
        except:
            pass
 
    def getDeviceID(self, maxlen, timeout = 100):
 
        return self.__devhandle.controlMsg(requestType = 0xa1,
                                           request = 0,
                                           value = self.__conf - 1,
                                           index = self.__alt + (self.__intf << 8),
                                           buffer = maxlen,
                                           timeout = timeout)
 
    def getPortStatus(self, timeout = 100):
 
        return self.__devhandle.controlMsg(requestType = 0xa1,
                                           request = 1,
                                           value = 0,
                                           index = self.__intf,
                                           buffer = 1,
                                           timeout = timeout)[0]
    def softReset(self, timeout = 100):
 
        self.__devhandle.controlMsg(requestType = 0x21,
                                       request = 2,
                                       value = 0,
                                       index = self.__intf,
                                       buffer = 0)
 
 
    def write(self, buffer, timeout = 100):
 
        return self.__devhandle.bulkWrite(self.__bulkout,
                                          buffer,
                                          timeout)
 
    def read(self, numbytes, timeout = 100):
 
        return self.__devhandle.bulkRead(self.__bulkin,
                                         numbytes,
                                         timeout)
 
class usbDispositivo:
 
    '''
    Modelo de datos de un dispositivo USB (tipo VO)
    '''
 
    def __init__(self,dispositivo):
 
        self.archivo = ''
        self.clase = ''
        self.subClase = ''
        self.protocolo = ''
        self.idFabricante = ''
        self.idProducto = ''
        self.version = ''
        self.descripcion = ''
        self.archivo = dispositivo.filename
        self.clase = dispositivo.deviceClass
        self.subClase = dispositivo.deviceSubClass
        self.protocolo = dispositivo.deviceProtocol
        self.idFabricante = dispositivo.idVendor
        self.idProducto = dispositivo.idProduct
        self.version = dispositivo.deviceVersion
 
        try:
            self.descripcion = dispositivo.open().getString(1,30)
        except:
            self.descripcion = ''
 
    def getArchivo(self):
        return self.archivo
 
    def getClase(self):
        return self.clase
 
    def getSubClase(self):
        return self.subClase
 
    def getProtocolo(self):
        return self.protocolo
 
    def getIdFabricante(self):
        return self.idFabricante
 
    def getIdProducto(self):
        return self.idProducto
 
    def getVersion(self):
        return self.version
 
    def getDescripcion(self):
        return self.descripcion

