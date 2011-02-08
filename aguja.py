#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import threading
import socket
#import queusb
import dbus

from math import hypot, sin, cos, pi
       
EVT_NEW_DATA_ID = wx.NewId()

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_NEW_DATA_ID, func)
        
class AcquireEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_NEW_DATA_ID)
        self.data = data

class Reloj(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(450, 400))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.worker = WorkerThread(self)
        self.Show(True)
        self.angle = -pi-60*pi/180
        self.subangle = (20*pi/180)
        self.alive=True
        EVT_RESULT(self, self.OnAcquireData)
        
    def OnResult(self,event):
        print "hubo un evento"
        #self.angle=0
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        size_x, size_y = self.GetClientSizeTuple()
        dc.SetDeviceOrigin(size_x/2, size_y/2)
        if (size_x < size_y):
            size=size_x
        else:
            size=size_y
        radius = hypot(size/4, size/4)
        x1 = radius*cos(self.angle)
        y1 = radius*sin(self.angle)
        x2 = (-radius/8)*cos(self.angle+self.subangle)
        y2 = (-radius/8)*sin(self.angle+self.subangle)
        x3 = (-radius/8)*cos(self.angle-self.subangle)
        y3 = (-radius/8)*sin(self.angle-self.subangle)
        pen = wx.Pen('#ac0cfc', 2, wx.SOLID)
        dc.SetPen(pen)
        dc.DrawCircle(0, 0, (radius+10))
        dc.DrawCircle(0, 0, (radius/10))
        dc.DrawPolygon(((x1,y1),(x2,y2),(x3,y3)))
        for marcas in range(-240,60,5):
            x1 = (radius-2)*cos(marcas*pi/180)
            y1 = (radius-2)*sin(marcas*pi/180)
            x2 = (radius-10)*cos(marcas*pi/180)
            y2 = (radius-10)*sin(marcas*pi/180)
            dc.DrawLine(x1,y1,x2,y2)
            
    def OnAquireData(self,evt):
        self.angle = evt.data
        

# Thread class that executes processing
class WorkerThread(threading.Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        
        self.start()

    def run(self):
        import usb.core
        import usb.util
        dev = usb.core.find(idVendor=0x1414, idProduct=0x2013)
        interface = dev.get_interface_altsetting()
        if dev.is_kernel_driver_active(interface.bInterfaceNumber) is True:
            dev.detach_kernel_driver(interface.bInterfaceNumber)
        dev.set_configuration()
        dev.reset()
        pesadas = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        cuenta=0.0
        valor_anterior=0
        while self._notify_window.alive:
            cadena = dev.read(0x81,32)
            if len(cadena)>30:
                peso = [chr(a) for a in cadena]
                gramos = int(peso[0])*1000+int(peso[1])*100+int(peso[2])*10+int(peso[3])
                pesadas.pop(0)
                pesadas.append(gramos)
                cuenta+=1
                if cuenta == 10:
                    cuenta = 0
                    valor=0
                    for a in pesadas:
                        valor+=a
                    valor = valor / len(pesadas)
                    if valor != valor_anterior:
                        print valor
                        valor_anterior = valor
                        rel.angle=valor*300*pi/720000-pi-60*pi/180
                        #wx.PostEvent(self._notify_window,wx.EVT_PAINT)   
        rel.angle=0
        
        #"""Run Worker Thread."""
        # This is the code executing in the new thread
        # Here's where the result would be returned (this is an
        # example fixed result of the number 10, but it could be
        # any Python object)
        #wx.PostEvent(self._notify_window, ResultEvent(10))      
                        
app = wx.App()
rel=Reloj(None, -1, 'Balanza')
app.MainLoop()
