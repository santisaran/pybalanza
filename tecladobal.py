#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import cStringIO
import base64
import threading
import random

tile_file = "images/base.png"

class puntero():
    def __init__(self,vector):
        self.vector=vector
        self.size=len(vector)
    def up(self):
        self.vector.insert(0,self.vector.pop())
        
    def down(self):
        self.vector.insert(-1,self.vector.pop(0))

class Panel1(wx.Panel):
    """ 
    class Panel1 creates a panel for the tile image
    fw and fh are the width and height of the base frame
    """
    def __init__(self, parent, id, fw, fh, tile_file):
        # create the panel
        wx.Panel.__init__(self, parent, id)
        # frame/panel width and height
        self.fw = fw
        self.fh = fh
        # load the wallpaper/tile file
        self.bmp1 = wx.Bitmap(tile_file)
        # do the wall papering ...
        wx.EVT_PAINT(self, self.on_paint)
        # now put a button on the panel, on top of wallpaper
        posh = (430,499,568,637)
        posv = (60,128,196,266)
        self.botones = ("images/btn1_peso.png","images/btn2_cont.png","images/btn3_cal.png","images/btn_tara.png",\
                        "images/btn4_vol.png", "images/btn5_den.png", "images/btn6.png",    "images/btn_uni.png",\
                        "images/btn7.png",     "images/btn8.png",     "images/btn9.png",    "images/btn_acep.png",\
                        "images/btn_up.png", "images/btn0.png",   "images/btn_down.png","images/btn._punto.png")
        self.unidades_peso = puntero([u"gr","kg","lb"])
        self.unidades_vol = puntero([u"cm³",u"dm³",u"in³"])
        self.unidades_den = puntero(["gr","kg","lb"])
        
        self.ptrpeso=0
        self.ptrvol=0
        self.ptrden=0
        
        self.estados= ("balanza","contador","calidad","volumen","densidad")
        self.estado = self.estados[0]
        self.unidad_peso = self.unidades_peso.vector[0]
        self.unidad_vol = self.unidades_vol.vector[0]
        self.unidad_den = self.unidades_den.vector[0]
        #~ for i in posh:
            #~ for j in posv:
                #~ a = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"btn1.png", wx.BITMAP_TYPE_ANY), pos=(i,j), style=0|wx.NO_BORDER )
                #~ a.SetBitmapSelected( wx.Bitmap( u"btn1_p.png", wx.BITMAP_TYPE_ANY ))
        
        self.pantalla = wx.TextCtrl( self, wx.ID_ANY, u"Peso: 0000 gr", pos=(72,95),size=(272,80), style=0|wx.TE_MULTILINE )
        self.pantalla.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
        
        #--------------------------------------------------------------#
        #-------------------    BOTONES     ---------------------------#
        #--------------------------------------------------------------#
        
        self.btn1 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[0], wx.BITMAP_TYPE_ANY), pos=(430,60), style=0|wx.NO_BORDER )
        self.btn1.SetBitmapSelected( wx.Bitmap( self.botones[0], wx.BITMAP_TYPE_ANY ))
        
        self.btn2 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[1], wx.BITMAP_TYPE_ANY), pos=(499,60), style=0|wx.NO_BORDER )
        self.btn2.SetBitmapSelected( wx.Bitmap( self.botones[1], wx.BITMAP_TYPE_ANY ))
        
        self.btn3 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[2], wx.BITMAP_TYPE_ANY), pos=(568,60), style=0|wx.NO_BORDER )
        self.btn3.SetBitmapSelected( wx.Bitmap( self.botones[2], wx.BITMAP_TYPE_ANY ))
        
        self.btn_tara = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[3], wx.BITMAP_TYPE_ANY), pos=(637,60), style=0|wx.NO_BORDER )
        self.btn_tara.SetBitmapSelected( wx.Bitmap( self.botones[3], wx.BITMAP_TYPE_ANY ))
        
        self.btn4 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[4], wx.BITMAP_TYPE_ANY), pos=(430,128), style=0|wx.NO_BORDER )
        self.btn4.SetBitmapSelected( wx.Bitmap( self.botones[4], wx.BITMAP_TYPE_ANY ))
        
        self.btn5 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[5], wx.BITMAP_TYPE_ANY), pos=(499,128), style=0|wx.NO_BORDER )
        self.btn5.SetBitmapSelected( wx.Bitmap( self.botones[5], wx.BITMAP_TYPE_ANY ))
        
        self.btn6 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[6], wx.BITMAP_TYPE_ANY), pos=(568,128), style=0|wx.NO_BORDER )
        self.btn6.SetBitmapSelected( wx.Bitmap( self.botones[6], wx.BITMAP_TYPE_ANY ))
        
        self.btn_uni = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[7], wx.BITMAP_TYPE_ANY), pos=(637,128), style=0|wx.NO_BORDER )
        self.btn_uni.SetBitmapSelected( wx.Bitmap( self.botones[7], wx.BITMAP_TYPE_ANY ))
        
        self.btn7 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[8], wx.BITMAP_TYPE_ANY), pos=(431,196), style=0|wx.NO_BORDER )
        #self.btn7.SetBitmapSelected( wx.Bitmap( u"btn1_p.png", wx.BITMAP_TYPE_ANY ))
        
        self.btn8 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[9], wx.BITMAP_TYPE_ANY), pos=(499,196), style=0|wx.NO_BORDER )
        self.btn8.SetBitmapSelected( wx.Bitmap( self.botones[9], wx.BITMAP_TYPE_ANY ))
        
        self.btn9 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[10], wx.BITMAP_TYPE_ANY), pos=(568,196), style=0|wx.NO_BORDER )
        self.btn9.SetBitmapSelected( wx.Bitmap( self.botones[10], wx.BITMAP_TYPE_ANY ))
        
        self.btn_acep = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[11], wx.BITMAP_TYPE_ANY), pos=(637,196), style=0|wx.NO_BORDER )
        self.btn_acep.SetBitmapSelected( wx.Bitmap( self.botones[11], wx.BITMAP_TYPE_ANY ))
        
        self.btn_down = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[12], wx.BITMAP_TYPE_ANY), pos=(430,266), style=0|wx.NO_BORDER )
        self.btn_down.SetBitmapSelected( wx.Bitmap( self.botones[12], wx.BITMAP_TYPE_ANY ))
        
        self.btn0 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[13], wx.BITMAP_TYPE_ANY), pos=(499,266), style=0|wx.NO_BORDER )
        self.btn0.SetBitmapSelected( wx.Bitmap( self.botones[13], wx.BITMAP_TYPE_ANY ))
        
        self.btn_up = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[14], wx.BITMAP_TYPE_ANY), pos=(568,266), style=0|wx.NO_BORDER )
        self.btn_up.SetBitmapSelected( wx.Bitmap( self.botones[14], wx.BITMAP_TYPE_ANY ))
        
        self.btn_fin = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[15], wx.BITMAP_TYPE_ANY), pos=(637,266), style=0|wx.NO_BORDER )
        self.btn_fin.SetBitmapSelected( wx.Bitmap( self.botones[15], wx.BITMAP_TYPE_ANY ))
        
        #--------------------------------------------------------------#
        #-------------------    Botones alternativos ------------------#
        #--------------------------------------------------------------#
        
        self.btn_save_tabla = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap( u"images/btn_gt.png", wx.BITMAP_TYPE_ANY), pos=(70,370), style=0|wx.NO_BORDER )
        #self.btn_save_tabla.SetBitmapSelected( wx.Bitmap( u"btn1_p.png", wx.BITMAP_TYPE_ANY ))
        
        self.btn_ver_tabla = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap( u"images/btn_vt.png", wx.BITMAP_TYPE_ANY), pos=(220,370), style=0|wx.NO_BORDER )
        #self.btn_ver_tabla.SetBitmapSelected( wx.Bitmap( u"btn1_p.png", wx.BITMAP_TYPE_ANY ))
        
        self.btn_ver_graf = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap( u"images/btn_vg.png", wx.BITMAP_TYPE_ANY), pos=(70,370), style=0|wx.NO_BORDER )
        #self.btn_ver_graf.SetBitmapSelected( wx.Bitmap( u"btn1_p.png", wx.BITMAP_TYPE_ANY ))
        
        
        
        #--------------------------------------------------------------#
        #-----------------  Asociación de eventos    ------------------#
        #--------------------------------------------------------------#
        #Botones teclado 4x4
        
        self.Bind(wx.EVT_BUTTON, self.OnBalanza, self.btn1) #
        self.Bind(wx.EVT_BUTTON, self.OnContador, self.btn2) #
        self.Bind(wx.EVT_BUTTON, self.OnCalidad, self.btn3) #
        self.Bind(wx.EVT_BUTTON, self.OnVolumen, self.btn4) #
        self.Bind(wx.EVT_BUTTON, self.OnDensidad, self.btn5) #
        self.Bind(wx.EVT_BUTTON, self.OnBalanza, self.btn6) #
        self.Bind(wx.EVT_BUTTON, self.OnBalanza, self.btn7) #
        self.Bind(wx.EVT_BUTTON, self.OnBalanza, self.btn8) #
        self.Bind(wx.EVT_BUTTON, self.OnBalanza, self.btn9) #
        self.Bind(wx.EVT_BUTTON, self.OnBalanza, self.btn0) #
        self.Bind(wx.EVT_BUTTON, self.OnTara, self.btn_tara) #
        self.Bind(wx.EVT_BUTTON, self.OnUnidad, self.btn_uni) #
        self.Bind(wx.EVT_BUTTON, self.OnAceptar, self.btn_acep) #
        self.Bind(wx.EVT_BUTTON, self.OnDown, self.btn_down) #
        self.Bind(wx.EVT_BUTTON, self.OnUp, self.btn_up) #
        self.Bind(wx.EVT_BUTTON, self.OnFin, self.btn_fin) #
        
        #botones alternativos
        
        self.Bind(wx.EVT_BUTTON, self.OnGTabla, self.btn_save_tabla)   #
        self.Bind(wx.EVT_BUTTON, self.OnVerTabla, self.btn_ver_tabla)  #
        self.Bind(wx.EVT_BUTTON, self.OnVerGrafico, self.btn_ver_graf) #
        
        #self.btn_save_tabla.Enable( False )
        #self.btn_save_tabla.Hide()
        #self.btn_ver_tabla.Enable(False)
        #self.btn_ver_tabla.Hide()
        self.btn_ver_graf.Enable(False)
        self.btn_ver_graf.Hide()
        
        self.Bind(wx.EVT_TIMER, self.OnTimeout)
        self.timer = wx.Timer(self)
        self.timer.Start(1500)
    
    #valor aleatorio para probar soft sinbalanza.
    def OnTimeout(self, evt):
        if self.estado=="balanza":
            self.pantalla.SetValue("Peso: " + str(random.randint(0, 4000)) + self.unidades_peso.vector[0])
        elif self.estado=="contador":
            self.pantalla.SetValue("Contador: " + str(random.randint(0, 4000)) + " pcs")
        
    def BtnsBal (self,guardar=True,ver=True,mostrar=True):
        """ Muestra/oculta los botones de la funcion pesar """
        self.btn_save_tabla.Enable(guardar)
        self.btn_save_tabla.Show(guardar)
        self.btn_ver_tabla.Enable(ver)
        self.btn_ver_tabla.Show(ver)
        self.btn_ver_graf.Enable(mostrar)
        self.btn_ver_graf.Show(mostrar)
    
    #------------------------------------------------------------------#
    #----------- Funciones asociadas a eventos ------------------------#
    #------------------------------------------------------------------#
    
    def OnBalanza(self,evt):
        """Acción al presionar boton 1/Balanza"""
        #print "balanza"
        if self.estado != "balanza":
            self.estado = "balanza"
            self.BtnsBal(True,True,False)
            evt.Skip()
    
    def OnContador(self,evt):
        """Acción al presionar boton 2/Contador"""
        if self.estado != "contador":
            self.estado = "contador"
            self.BtnsBal(False,True,False)
        evt.Skip()
        
    def OnCalidad(self,evt):
        """Acción al presionar boton 3/Calidad"""
        if self.estado != "calidad":
            self.estado = "calidad"
            self.BtnsBal(False,True,True)
        evt.Skip()
        
    def OnVolumen(self,evt):
        """Acción al presionar boton 3/Calidad"""
        if self.estado != "volumen":
            self.estado = "volumen"
            self.BtnsBal(False,True,True)
        evt.Skip()
        
    def OnDensidad(self,evt):
        """Acción al presionar boton 3/Calidad"""
        if self.estado != "densidad":
            self.estado = "densidad"
            self.BtnsBal(False,True,True)
        evt.Skip()
        
    def OnUnidad(self,evt):
        """Acción al presionar unidad"""
        print "cambiode unidad"
        if self.estado=="balanza":
            self.unidades_peso.up()
        evt.Skip()
        
    def OnTara(self,evt):
        """Acción al presionar botón Tara"""
        evt.Skip()
        
    def OnAceptar(self,evt):
        """Acción al presionar botón Aceptar"""
        evt.Skip()
        
    def OnDown(self,evt):
        """Acción al presionar botón Down"""
        evt.Skip()
        
    def OnUp(self,evt):
        """Acción al presionar botón up"""
        evt.Skip()
        
    def OnFin(self,evt):
        """Acción al presionar botón up"""
        evt.Skip()
        
    
    
    def OnGTabla(self,evt):
        """Acción al presionar boton Guardar Tabla"""
        evt.Skip()
        
    def OnVerTabla(self,evt):
        """Acción al presionar boton Ver Tabla"""
        evt.Skip()
    
    def OnVerGrafico(self,evt):
        """Acción al presionar boton Ver Gráfico"""
        evt.Skip()
    
    def on_paint(self, event=None):
        # create paint surface
        dc = wx.PaintDC(self)
        dc.Clear()
        #dc.SetBackgroundMode(wx.TRANSPARENT)
        # get image width and height
        iw = self.bmp1.GetWidth()
        ih = self.bmp1.GetHeight()
        # tile/wallpaper the image across the canvas
        for x in range(0, self.fw, iw):
            for y in range(0, self.fh, ih):
                dc.DrawBitmap(self.bmp1, x, y, True)
                
    #------------------------------------------------------------------#
    #------------------------------------------------------------------#
    #------------------------------------------------------------------#
class ThreadLector(threading.Thread):
    """
    Thread que se queda escuchando datos en el puerto de conexión.
    Y mantiene con vida la conexión
    """
    def __init__(self, threadNum, window, conector):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.window = window
        self.conector = conector

    def stop(self):
        self.window.s.close()
    
    def run(self):  
        """thread que se encarga de recibir los datos que vienen de la balanza
        Por medio de una conexión TCP"""
        mensaje = ""
        while self.window.alive:
            try:
                mensaje = self.conector.s.recv(1024)
            except socket.timeout:
                continue
            if mensaje != "":
                if mensaje == "life":
                    self.conector.writer("YESILIVE")
                    #protocolo propio de este programa para mantener viva la 
                    #conexió y detectar posibles cortes
                elif mensaje[0:4] == "temp":    #recibe tempXX.X
                    TEMP = mensaje[4:8]
                elif mensaje[0:4] == "dwpt":    #recibe dwptXX.X
                    self.DP = mensaje[4:8]
                else:
                    wx.PostEvent(self.window, AcquireEvent(mensaje[:-2]))   
        print "conexión cerrada"

app = wx.PySimpleApp()
# create a window/frame instance, no parent, -1 is default ID
fw = 756
fh = 484
frame1 = wx.Frame(None, -1, "Balanza", size=(fw, fh))
# create a panel class instance
panel1 = Panel1(frame1, -1, fw, fh, tile_file)
frame1.Show(True)
# start the event loop
app.MainLoop()
