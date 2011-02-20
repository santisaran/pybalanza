#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import threading
import random
import sys
import os
import time

#ventana para graficar calidad:
import grafico
from decimal import Decimal as dec
import list_report

sep = os.sep
if sys.platform=="linux2":
    a=0
elif sys.platform=="win32":
    a=5
tile_file = "images"+sep+"base.png"

BALANZA = True
#posiciones de los botones del teclado
def posbtns(x,y):
    posh = (430+a,499+a,568+a,637+a)
    posv = (60+a,128+a,196+a,266+a)
    return (posh[x],posv[y])
    
#----------------------------------------------------------------------#
#----------------------------------------------------------------------#
#------------------ Evento al llegar datos por USB --------------------#
#----------------------------------------------------------------------#
#----------------------------------------------------------------------#

EVT_NEW_DATA_ID = wx.NewId()

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_NEW_DATA_ID, func)

class AcquireEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_NEW_DATA_ID)
        self.data = data

#----------------------------------------------------------------------#
#------------------ ------ -- ------ -- ----- -- ----------------------#
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
#-------------------Clase para manejar unidades -----------------------#
#----------------------------------------------------------------------#
class puntero():
    def __init__(self,vector):
        self.vector=vector
        self.size=len(vector)
    def up(self):
        self.vector.insert(0,self.vector.pop())
    def down(self):
        self.vector.insert(-1,self.vector.pop(0))
#----------------------------------------------------------------------#
#----------------------------------------------------------------------#
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
#----------------------Panel Principal --------------------------------#
#----------------------------------------------------------------------#
class Panel1(wx.Panel):
    def __init__(self, parent, id, fw, fh, tile_file):
        # crea el panel
        wx.Panel.__init__(self, parent, id)
        # frame/panel ancho y alto
        self.fw = fw
        self.fh = fh
        # cargo imagen de fondo de pantalla
        self.bmp1 = wx.Bitmap(tile_file)
        # pinto imagen el el fondo.
        wx.EVT_PAINT(self, self.on_paint)

        posh = (430,499,568,637)
        posv = (60,128,196,266)
        #lista de imágenes para los botones
        self.botones = ("images"+sep+"btn1_peso.png","images"+sep+"btn2_cont.png","images"+sep+"btn3_cal.png","images"+sep+"btn_tara.png",\
                        "images"+sep+"btn4_vol.png", "images"+sep+"btn5_den.png", "images"+sep+"btn6.png",    "images"+sep+"btn_uni.png",\
                        "images"+sep+"btn7.png",     "images"+sep+"btn8.png",     "images"+sep+"btn9.png",    "images"+sep+"btn_acep.png",\
                        "images"+sep+"btn_up.png", "images"+sep+"btn0.png",   "images"+sep+"btn_down.png","images"+sep+"btn._punto.png")
        self.botones_press = [i[:-4]+"_press.png" for i in self.botones]
        self.unidades_peso = puntero([u"gr","kg","lb"])
        self.unidades_vol = puntero([u"cm3",u"dm3",u"in3"])
        self.unidades_den = puntero(["g/cm3","lb/in3"])
        
        self.ptrpeso=0
        self.ptrvol=0
        self.ptrden=0
        self.tara = 0
        self.peso = None
        #tabla de valores de balanza
        self.l_bal = []
        #tabla de valores de muestras en función balanza
        self.l_muestras = []
        #lista de volúmenes para tabla
        self.l_vol = []
        #lista de densidades para tabla
        self.l_den = []
        #lista de calidad
        self.l_calidad= []
        self.idact = "0"
        
        self.estados= ("balanza","contador","calidad","volumen","densidad")
        self.estado = self.estados[0]
        self.unidad_peso = self.unidades_peso.vector[0]
        self.unidad_vol = self.unidades_vol.vector[0]
        self.unidad_den = self.unidades_den.vector[0]
        self.uni = "gr"
        self.uni_vol = "cm3"
        self.uni_den = "g/cm3"
        #~ for i in posh:
            #~ for j in posv:
                #~ a = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"btn1.png", wx.BITMAP_TYPE_ANY), pos=(i,j), style=0|wx.NO_BORDER )
                #~ a.SetBitmapSelected( wx.Bitmap( u"btn1_p.png", wx.BITMAP_TYPE_ANY ))
        
        self.pantalla = wx.TextCtrl( self, wx.ID_ANY, u"Peso: 0000 gr", pos=(72,95),size=(272,80), style=0|wx.TE_MULTILINE )
        self.pantalla.SetFont( wx.Font( 15, 70, 90, 90, False, wx.EmptyString ) )
        
        #--------------------------------------------------------------#
        #-------------------    BOTONES     ---------------------------#
        #--------------------------------------------------------------#
        
        self.btn1 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[0], wx.BITMAP_TYPE_PNG), pos=posbtns(0,0), style=0|wx.NO_BORDER )
        self.btn1.SetBitmapSelected( wx.Bitmap( self.botones_press[0], wx.BITMAP_TYPE_ANY ))
        self.btn1.SetTransparent(200)
        
        self.btn2 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[1], wx.BITMAP_TYPE_ANY), pos=posbtns(1,0), style=0|wx.NO_BORDER )
        self.btn2.SetBitmapSelected( wx.Bitmap( self.botones_press[1], wx.BITMAP_TYPE_ANY ))
        
        self.btn3 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[2], wx.BITMAP_TYPE_ANY), pos=posbtns(2,0), style=0|wx.NO_BORDER )
        self.btn3.SetBitmapSelected( wx.Bitmap( self.botones_press[2], wx.BITMAP_TYPE_ANY ))
        
        self.btn_tara = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[3], wx.BITMAP_TYPE_ANY), pos=posbtns(3,0), style=0|wx.NO_BORDER )
        self.btn_tara.SetBitmapSelected( wx.Bitmap( self.botones_press[3], wx.BITMAP_TYPE_ANY ))
        
        self.btn4 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[4], wx.BITMAP_TYPE_ANY), pos=posbtns(0,1), style=0|wx.NO_BORDER )
        self.btn4.SetBitmapSelected( wx.Bitmap( self.botones_press[4], wx.BITMAP_TYPE_ANY ))
        
        self.btn5 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[5], wx.BITMAP_TYPE_ANY), pos=posbtns(1,1), style=0|wx.NO_BORDER )
        self.btn5.SetBitmapSelected( wx.Bitmap( self.botones_press[5], wx.BITMAP_TYPE_ANY ))
        
        self.btn6 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[6], wx.BITMAP_TYPE_ANY), pos=posbtns(2,1), style=0|wx.NO_BORDER )
        self.btn6.SetBitmapSelected( wx.Bitmap( self.botones_press[6], wx.BITMAP_TYPE_ANY ))
        
        self.btn_uni = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[7], wx.BITMAP_TYPE_ANY), pos=posbtns(3,1), style=0|wx.NO_BORDER )
        self.btn_uni.SetBitmapSelected( wx.Bitmap( self.botones_press[7], wx.BITMAP_TYPE_ANY ))
        
        self.btn7 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[8], wx.BITMAP_TYPE_ANY), pos=posbtns(0,2), style=0|wx.NO_BORDER )
        self.btn7.SetBitmapSelected( wx.Bitmap( self.botones_press[8], wx.BITMAP_TYPE_ANY ))
        
        self.btn8 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[9], wx.BITMAP_TYPE_ANY), pos=posbtns(1,2), style=0|wx.NO_BORDER )
        self.btn8.SetBitmapSelected( wx.Bitmap( self.botones_press[9], wx.BITMAP_TYPE_ANY ))
        
        self.btn9 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[10], wx.BITMAP_TYPE_ANY), pos=posbtns(2,2), style=0|wx.NO_BORDER )
        self.btn9.SetBitmapSelected( wx.Bitmap( self.botones_press[10], wx.BITMAP_TYPE_ANY ))
        
        self.btn_acep = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[11], wx.BITMAP_TYPE_ANY), pos=posbtns(3,2), style=0|wx.NO_BORDER )
        self.btn_acep.SetBitmapSelected( wx.Bitmap( self.botones_press[11], wx.BITMAP_TYPE_ANY ))
        
        self.btn_down = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[12], wx.BITMAP_TYPE_ANY), pos=posbtns(0,3), style=0|wx.NO_BORDER )
        self.btn_down.SetBitmapSelected( wx.Bitmap( self.botones_press[12], wx.BITMAP_TYPE_ANY ))
        
        self.btn0 = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[13], wx.BITMAP_TYPE_ANY), pos=posbtns(1,3), style=0|wx.NO_BORDER )
        self.btn0.SetBitmapSelected( wx.Bitmap( self.botones_press[13], wx.BITMAP_TYPE_ANY ))
        
        self.btn_up = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[14], wx.BITMAP_TYPE_ANY), pos=posbtns(2,3), style=0|wx.NO_BORDER )
        self.btn_up.SetBitmapSelected( wx.Bitmap( self.botones_press[14], wx.BITMAP_TYPE_ANY ))
        
        self.btn_fin = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( self.botones[15], wx.BITMAP_TYPE_ANY), pos=posbtns(3,3), style=0|wx.NO_BORDER )
        self.btn_fin.SetBitmapSelected( wx.Bitmap( self.botones_press[15], wx.BITMAP_TYPE_ANY ))
        
        #--------------------------------------------------------------#
        #-------------------    Botones alternativos ------------------#
        #--------------------------------------------------------------#
        
        self.btn_save_tabla = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap( u"images"+sep+"btn_gt.png", wx.BITMAP_TYPE_ANY), pos=(70,370), style=0|wx.NO_BORDER )
        self.btn_save_tabla.SetBitmapSelected( wx.Bitmap( u"images"+sep+"btn_gt_press.png", wx.BITMAP_TYPE_ANY ))
        
        self.btn_ver_tabla = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap( u"images"+sep+"btn_vt.png", wx.BITMAP_TYPE_ANY), pos=(220,370), style=0|wx.NO_BORDER )
        self.btn_ver_tabla.SetBitmapSelected( wx.Bitmap( u"images"+sep+"btn_vt_press.png", wx.BITMAP_TYPE_ANY ))
        
        self.btn_ver_graf = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap( u"images"+sep+"btn_vg.png", wx.BITMAP_TYPE_ANY), pos=(70,370), style=0|wx.NO_BORDER )
        self.btn_ver_graf.SetBitmapSelected( wx.Bitmap( u"images"+sep+"btn_vg_press.png", wx.BITMAP_TYPE_ANY ))
        
        
        
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
        
        EVT_RESULT(self, self.OnAcquireData)
        self.Bind(wx.EVT_MENU_CLOSE, self.OnClosePanel)
        parent.Bind(wx.EVT_CLOSE, self.OnClosePanel)
        
        #self.btn_save_tabla.Enable( False )
        #self.btn_save_tabla.Hide()
        #self.btn_ver_tabla.Enable(False)
        #self.btn_ver_tabla.Hide()
        self.btn_ver_graf.Enable(False)
        self.btn_ver_graf.Hide()
        
        parent.Centre( wx.BOTH )
        self.alive = True
        self.thread = ThreadLector(0, self)
        self.thread.start()
        TIMER_ID = 100
        self.timer = wx.Timer(self,TIMER_ID)  # message will be sent to the panel
        self.timer.Start(100,True)  # x100 milliseconds
        wx.EVT_TIMER(self, TIMER_ID, self.on_timer)
        #self.Bind(wx.EVT_TIMER, self.on_timer)
        
        #timer para autotara cuando peso es -1
        #~ self.TIMERTARAID = 200
        #~ self.timerautotara = wx.Timer(self,self.TIMERTARAID)
        #~ wx.EVT_TIMER(self, self.TIMERTARAID, self.OnAutotara)
        #~ self.autotara = 0
        
        self.voldb = False
        self.volaceptado = False
        self.den_acep = False
        self.den_db = False

#autotara al inicio. cada 100 milisegundos chekea el valor de peso. hasta que
#sea distinto de None.
    def on_timer(self,event):
        if self.peso==None:
            self.timer.Start(100,True)
        else:
            self.tara=int(self.peso)
        event.Skip()

    def OnAutotara(self,evt):
        self.autotara=self.autotara+1
            
        pass

    def OnAcquireData(self,evt):
        """Evento de recepción de datos"""
        if self.uni=="lb":
            peso=round(dec((dec(dec(int(evt.data)-self.tara)/4096*4000)/dec("453592.37"))*1000),3)
        elif self.uni=="kg":
            peso=round(dec(dec(int(evt.data)-self.tara)/4096*4000)/dec("1000"),3)
        else:
            peso= int(dec(int(evt.data)-self.tara)/4096*4000)
        self.valoractual = str(int(dec(int(evt.data)-self.tara)/4096*4000))
        if int(self.valoractual)==-1:
            self.autotara=self.autotara+1
            if self.autotara == 25:
                self.tara = int(evt.data)
                self.autotara = 0
        else:
            self.autotara = 0
            
        if int(self.valoractual) < -1:
            self.pantalla.SetValue("Requiere tara")
            self.peso=evt.data
        else:
            self.peso = evt.data
            if self.estado == "balanza":
                #para almacenar en tabla guardo directo el valor de la balanza.
                self.pantalla.SetValue(u"Peso: " + str(peso) + " " + self.uni)
            
            elif self.estado == "contador":
                if not self.coloque:
                    #para almacenar en tabla guardo directo el valor de la balanza.
                    self.pantalla.SetValue(u"Peso: " + str(peso) + self.uni + "\nColoque Muestra")
                    #variable con el valor actual en pantalla.
                    
                else:
                    self.cantidad = int(self.valoractual)/int(self.muestra)
                    self.pantalla.SetValue(u"Cant: " + str(self.cantidad) + "\nUnidades")
            elif self.estado == "volumen":
                if self.volaceptado:
                    if self.uni_vol == "in3":
                        peso = round(dec(peso)/dec("16.387064"),2)
                    if self.uni_vol == "dm3":
                        peso = dec(int(peso))/1000
                    self.pantalla.SetValue(u"Peso: " + str(peso) + " " + self.uni_vol + "\nColoque Material")
                else:
                    self.pantalla.SetFont( wx.Font( 15, 70, 90, 90, False, wx.EmptyString ) )
                    self.pantalla.SetValue(u"Peso: " + str(peso) + self.uni + "\nInserte recipiente, Tare\ny acepte")
            elif self.estado == "densidad":
                if self.den_db:
                    if self.den_acep:
                        densidad = 0
                        try:
                            mostrar = round(dec(self.pesoden)/dec(peso),3)
                        except:
                            mostrar = ""
                        if mostrar<0:
                            mostrar = ""
                        elif mostrar!="":
                            self.densidadactual=mostrar
                            if self.uni_den == "lb/in3":
                                densidad = round(dec(str(mostrar)) / dec("27.679905"),3)
                            else:
                                densidad = mostrar
                        self.pantalla.SetValue(u"Peso: " + str(densidad) + " " + self.uni_den + "\nColoque material a medir densidad")
                    else:
                        self.pantalla.SetValue(u"Peso: " + str(peso) + " " + self.uni + "\nColoque Recipiente con Agua tare y acepte")
                else:
                    self.pantalla.SetValue(u"Peso: " + str(peso) + self.uni + "\nColoque material a medir\n densidad y acepte")
            elif self.estado == "calidad":
                self.pantalla.SetValue(u"Peso: " + str(peso) + " " + self.uni + "\nMuestra = " + str(self.idact)+"\nColoque muestras")
              
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
    
    def OnClosePanel(self,evt):
        """cerrando ventana"""
        self.alive=False
        self.thread.join()
        evt.Skip()
    
    def OnBalanza(self,evt):
        """Acción al presionar boton 1/Balanza"""
        #print "balanza"
        self.idact = 1
        if self.estado != "balanza":
            self.voldb = False
            self.volaceptado = False
            self.den_acep = False
            self.den_db = False
            self.estado = "balanza"
            self.BtnsBal(True,True,False)
            evt.Skip()
    
    def OnContador(self,evt):
        """Acción al presionar boton 2/Contador"""
        #if self.estado != "contador":
        self.estado = "contador"
        self.voldb = False
        self.volaceptado = False
        self.den_acep = False
        self.den_db = False        
        self.coloque = False
        self.pantalla.SetValue("Peso: "+self.valoractual+self.uni+"\nColoque Muestra") 
        self.BtnsBal(True,True,False)
        #else:
            #self.coloque = False
            
        evt.Skip()
        
    def OnCalidad(self,evt):
        """Acción al presionar boton 3/Calidad"""
        if self.estado != "calidad":
            self.idact=0
            self.estado = "calidad"
            self.voldb = False
            self.volaceptado = False
            self.den_acep = False
            self.den_db = False
            self.BtnsBal(False,True,True)
        evt.Skip()
        
    def OnVolumen(self,evt):
        """Acción al presionar boton 3/Calidad"""
        self.idact = 1
        self.volaceptado = False
        self.den_acep = False
        self.den_db = False
        self.voldb = True
        if self.estado != "volumen":
            self.estado = "volumen"
            self.BtnsBal(True,True,False)
        evt.Skip()
        
    def OnDensidad(self,evt):
        """Acción al presionar boton 3/Calidad"""
        self.idact=1
        #self.den_db = True
        if self.estado != "densidad":
            self.voldb = False
            self.volaceptado = False
            self.den_acep = False
            self.den_db = False
            self.estado = "densidad"
            self.BtnsBal(True,True,False)
        evt.Skip()
        
    def OnUnidad(self,evt):
        """Acción al presionar unidad"""
        if (self.estado=="balanza") or (self.estado=="calidad") or (self.estado=="contador"):
            self.unidades_peso.up()
            self.uni = self.unidades_peso.vector[0]
            wx.PostEvent(self, AcquireEvent(str(self.peso)))
        elif self.estado=="volumen":
            self.unidades_vol.up()
            self.uni_vol = self.unidades_vol.vector[0]
        elif self.estado=="densidad":
            self.unidades_den.up()
            self.uni_den = self.unidades_den.vector[0]
        evt.Skip()
        
    def OnTara(self,evt):
        """Acción al presionar botón Tara"""
        self.tara = int(self.peso)
        wx.PostEvent(self, AcquireEvent(str(self.peso)))
        evt.Skip()
        
    def OnAceptar(self,evt):
        """Acción al presionar botón Aceptar"""
        if self.estado == "contador":
            if not self.coloque:
                if dec(self.valoractual)>0:
                    self.muestra = int(self.valoractual)
                    self.coloque=True
                    self.pantalla.SetValue("Peso: "+self.valoractual+self.uni+"\nColoque conjunto") 
        elif self.estado == "volumen":
            if self.voldb == True:
                self.voldb = False
                self.volaceptado = True
        elif self.estado == "densidad":
            """está en función densidad"""
            if self.den_db:
                if self.den_acep == False:
                    self.den_db = True
                    self.den_acep = True
                else:
                    self.den_acep = False
                    self.den_db = False
            else:
                #self.pesoden es el peso al que se le calcula la densidad
                #esto se lo que hace con el primer aceptar
                self.pesoden=int(self.valoractual)
                self.den_db = True
                self.den_acep = False
        elif self.estado == "calidad":
            self.idact = str(int(self.idact)+1)
            self.l_calidad.append([str(self.idact),str(self.valoractual),time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())])
        evt.Skip()
        
    def OnDown(self,evt):
        """Acción al presionar botón Down"""
        evt.Skip()
        
    def OnUp(self,evt):
        """Acción al presionar botón up"""
        evt.Skip()
        
    def OnFin(self,evt):
        """Acción al presionar botón up"""
        self.voldb = False
        self.volaceptado = False
        self.den_acep = False
        self.den_db = False
        #tabla de valores de balanza
        self.l_bal = []
        #tabla de valores de muestras en función balanza
        self.l_muestras = []
        #lista de volúmenes para tabla
        self.l_vol = []
        #lista de densidades para tabla
        #self.l_den = []
        #lista de calidad
        self.l_calidad= []
        self.idact = "0"
        self.OnBalanza(evt)
        self.idact=0
        evt.Skip()

    def OnGTabla(self,evt):
        """Acción al presionar boton Guardar Tabla"""
        if self.estado=="balanza":
            self.idact =str(int(self.idact)+1)  
            self.l_bal.append([str(self.idact),self.valoractual,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())])
        elif self.estado == "contador":
            if self.coloque:
                self.idact =str(int(self.idact)+1)
                self.l_muestras.append([str(self.idact),str(self.muestra),str(self.valoractual),str(self.cantidad),time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())])
        elif self.estado == "volumen":
            if self.volaceptado:
                self.idact =str(int(self.idact)+1)
                self.l_vol.append([str(self.idact),self.peso,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())])
        elif self.estado == "densidad":
            if self.den_db and self.den_acep:
                self.idact =str(int(self.idact)+1)
                #guarda en tabla ID, Volumen, Peso, Densidad, Timestamp
                self.l_den.append([str(self.idact),str(self.valoractual),\
                    str(self.pesoden),str(self.densidadactual),\
                    time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())])
        evt.Skip()
        
    def OnVerTabla(self,evt):
        """Acción al presionar boton Ver Tabla"""
        if self.estado == "balanza":
            frame = list_report.ListaFrame(self,self.l_bal,"balanza",title="Lista de Muestras")
            frame.Show()
        elif self.estado == "contador":
            frame = list_report.ListaFrame(self,self.l_muestras,"contador",["ID","Peso x Unidad","Peso del Conjunto","Unidades","Timestamp"],"lista de muestras")
            frame.Show()
        elif self.estado == "volumen":
            if self.volaceptado:
                frame = list_report.ListaFrame(self,self.l_vol,"volumen",["ID","Volumen","Timestamp"],"Lista de Volúmenes")
                frame.Show()
        elif self.estado == "densidad":
            if self.den_db and self.den_acep:
                frame = list_report.ListaFrame(self,self.l_den,"densidad",["ID","Volumen","peso","densidad","TimeStamp"],"Lista de densidades")
                frame.Show()
        elif self.estado == "calidad":
            frame = list_report.ListaFrame(self,self.l_calidad,"calidad",["ID","Peso","Timestamp"],"Lista Calidad")
            frame.Show()
        evt.Skip()
    
    def OnVerGrafico(self,evt):
        """Acción al presionar boton Ver Gráfico"""
        grafico.VerGrafico(None, -1, 'Puntos Medidos',self.l_calidad)
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
    
    def sample_handler(self,data):
        global contador
        if contador == 10:
            contador = 0
            if BALANZA: 
                peso = int(chr(data[1]))*1000 + int(chr(data[2]))*100 + int(chr(data[3]))*10 +int(chr(data[4]))
                wx.PostEvent(self, AcquireEvent(str(peso)))
            else:
                wx.PostEvent(self, AcquireEvent(str(data[1])))
        contador+=1
    
    #------------------------------------------------------------------#
    #------------------------------------------------------------------#
    #------------------------------------------------------------------#
    
    def BorrarListas(self,evt):
        """borra las listas de valores que existan, es llamada desde list_report"""
        self.l_bal = []
        self.l_muestras = []
        self.l_vol = []
        self.l_den = []
        self.l_calidad = []
        self.idact = 0

class ThreadLector(threading.Thread):
    """
    Thread que se queda escuchando datos en el puerto de conexión.
    Y mantiene con vida la conexión
    """
    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.window = window

    def stop(self):
        pass
    
    def run(self):  
        """thread que se encarga de recibir los datos que vienen de la balanza
        Por medio de una conexión USB"""
        global contador
        
        if sys.platform=="win32":
            from pywinusb import hid
            if BALANZA:
                filtro = hid.HidDeviceFilter(vendor_id=0x1414,product_id=0x2013)
            else:
                filtro = hid.HidDeviceFilter(vendor_id=0x1345,product_id=0x1000)
            balanza = filtro.get_devices()
            balanza = balanza[0]
            contador=0
            try:
                balanza.open()
                balanza.set_raw_data_handler(self.window.sample_handler)
                while balanza.is_plugged() and self.window.alive:
                    time.sleep(1)
            finally:
                balanza.close()
                
        elif sys.platform == "linux2":
            import usb.core
            import usb.util
            if BALANZA:
                dev = usb.core.find(idVendor=0x1414, idProduct=0x2013)
            else:
                dev =  usb.core.find(idVendor=0x1345, idProduct=0x1000)
            interface = dev.get_interface_altsetting()
            if dev.is_kernel_driver_active(interface.bInterfaceNumber) is True:
                dev.detach_kernel_driver(interface.bInterfaceNumber)
            dev.set_configuration()
            dev.reset()
            pesadas = [0,0,0,0,0,0,0,0,0,0]
            cuenta=0.0
            valor_anterior=0
            while self.window.alive:
                cadena = dev.read(0x81,32)
                if len(cadena)>30:
                    
                    peso = [chr(a) for a in cadena]
                    if BALANZA:
                        gramos = (int(peso[0])*1000+int(peso[1])*100+int(peso[2])*10+int(peso[3]))
                    else:
                        gramos = cadena[0]
                    pesadas.pop(0)
                    pesadas.append(gramos)
                    cuenta+=1
                    if cuenta == 10:
                        cuenta = 0
                        valor=0
                        for a in pesadas:
                            valor+=a
                        valor = valor / len(pesadas)
                        wx.PostEvent(self.window, AcquireEvent(str(valor)))
                            
           
app = wx.App(0)
# create a window/frame instance, no parent, -1 is default ID
fw = 756
fh = 484
if sys.platform == "win32":
    fwadic = 8
    fhadic = 28
else:
    fwadic = 0
    fhadic = 0
frame1 = wx.Frame(None, -1, "Balanza", size=(fw+fwadic, fh+fhadic))
# create a panel class instance
panel1 = Panel1(frame1, -1, fw, fh, tile_file)
frame1.Show(True)

# start the event loop
app.MainLoop()
