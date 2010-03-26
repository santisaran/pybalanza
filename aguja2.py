#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import threading
import socket
#import queusb
import dbus

from math import hypot, sin, cos, pi

class Reloj(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(450, 400))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.worker = WorkerThread(self)
        self.Show(True)
        self.angle = -pi-60*pi/180
        self.subangle = (20*pi/180)
        
        
    def OnResult(self,event):
        print "hubo un evento"
        #self.angle=0
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        size_x, size_y = self.GetClientSizeTuple()
        dc.SetDeviceOrigin(size_x/2, size_y/2)
        radius = hypot(size_x/4, size_y/4)
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
        s = socket.socket()
        s.bind(("localhost", 9999))
        s.listen(1)
        sc, addr = s.accept()
        while True:
            recibido = sc.recv(32)
            
            if recibido == "quit":
                break
            print recibido+"\r",
            peso=int(recibido)
            rel.angle=peso*300*pi/720000-pi-60*pi/180
            rel.OnPaint(wx.EVT_PAINT)
        print "Recibido:", recibido
        sc.send(recibido)
        print "adios"
        rel.angle=0
        sc.close()
        s.close()

        #"""Run Worker Thread."""
        # This is the code executing in the new thread
        # Here's where the result would be returned (this is an
        # example fixed result of the number 10, but it could be
        # any Python object)
        #wx.PostEvent(self._notify_window, ResultEvent(10))      
                        
app = wx.App()
rel=Reloj(None, -1, 'Balanza')
app.MainLoop()
