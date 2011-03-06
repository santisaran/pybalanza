#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import wx
import random
data = []
for i in range(20):
    data.append([str(i),random.randint(650,1000)])
#muestras = ('10', '20', '30')
class prosdata():
    def __init__(self,datos):
        self.data=datos
        
        #valor máximo
        self.maxim = int(max(datos))
        #valor minimo
        self.mini = int(min(datos))
        #tamaño cuantas piezas fueron pesadas
        self.size = int(len(datos))
        #diferencia entre minima y máxima para autoescalar el gráfico
        self.dif = int(self.maxim)-int(self.mini)
        #promedio 
        self.prom = float(sum(self.data))/(len(datos))
        #desvío medio.
        self.desmed = float(sum([abs(i-self.prom) for i in self.data]))/self.size
        
class LineChart(wx.Window): 
    def __init__(self, parent,tabla=data):
        wx.Window.__init__(self, parent)
        self.padre = parent
        self.SetBackgroundColour('WHITE')
        self.datos = prosdata(tabla)
        self.InitBuffer()        

        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

########################################################################
#               Eventos de botones y redibujado                        #
########################################################################

    def OnSize(self, evt):
        # When the window size changes we need a new buffer.
        self.Refresh()  # si no se pone este refresh, solo se escribe el área nueva
        self.InitBuffer()
        
    def OnPaint(self, event):
        #self.Refresh()
        dc = wx.BufferedPaintDC(self, self.buffer)

########################################################################

    def InitBuffer(self):
        """Create the buffer bitmap to be the same size as the window,\
            then draw our graph to it.  Since we use wx.BufferedDC
            whatever is drawn to the buffer is also drawn to the window."""
        w, h = self.GetClientSize()
        self.alto = h-30
        self.ancho = w-20
        self.buffer = wx.EmptyBitmap(w, h)
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.DrawGraph(dc)

    def DrawGraph(self,dc):
        dc.SetBackground(wx.Brush('WHITE'))
        dc.Clear()
        dc.SetDeviceOrigin(45, self.alto-0)
        dc.SetAxisOrientation(True, True)
        dc.SetPen(wx.Pen('WHITE'))
        #dc.SetBrush(wx.Brush('WHITE',wx.SOLID))
        #dc.DrawRectangle(1, 1, self.alto-10, self.ancho-10)
        self.DrawAxis(dc)
        self.DrawGrid(dc)
        self.DrawTitle(dc)
        self.DrawData(dc)

    def DrawAxis(self, dc):
        dc.SetPen(wx.Pen('#0AB1FF'))
        font =  dc.GetFont()
        font.SetPointSize(8)
        dc.SetFont(font)
        
        #Eje X
        dc.DrawLine(1, 1, self.ancho-30, 1)
        dc.DrawLine(self.ancho-30,1,self.ancho-35,-4)
        dc.DrawLine(self.ancho-30,1,self.ancho-35,+3)
        dc.DrawText("Muestras",self.ancho-dc.GetTextExtent("Muestras")[0]-30,1)
        
        #Eje y
        dc.DrawLine(1, 1, 1, self.alto-20)
        dc.DrawLine(1, self.alto-20, -4, self.alto-25)
        dc.DrawLine(1, self.alto-20, 5, self.alto-25)
        dc.DrawText("Peso",-dc.GetTextExtent("Peso")[0]-2, self.alto-20-dc.GetTextExtent("Muestras")[1])
        
        alto = self.alto-50
        minimo = alto*0.1
        maximo = alto*0.9
        ancho = self.ancho-30
        dif = maximo - minimo
        if self.datos.dif!=0:
            self.coordmin = int(dif/self.datos.dif*self.datos.mini) #valor minimo en el grafico.
            self.coordmax = int(dif/self.datos.dif*self.datos.maxim) #valor maximo en el gráfico.   
        else:
            self.coordmin = minimo
            self.coordmax = maximo
            
        self.diven = 5 # dividir en tantas partes el eje y
        for i in range(0,self.diven+1,1):
            dc.DrawText("%.2f"%(float(i*self.datos.dif)/self.diven+self.datos.mini), -45, i*dif/self.diven+minimo+5)
            dc.DrawLine(4,i*dif/self.diven+minimo, -5,i*dif/self.diven+minimo)
            
            
        for i in range(1, ancho,int(round(ancho/len(data)))):
            dc.DrawLine(i, 2, i, -5)
        
        for i in range(0,self.datos.size,self.datos.size/5 if self.datos.size/5>=1 else 1):
            dc.DrawText(str(i+1),ancho/self.datos.size*i-10,-10)

    def DrawGrid(self, dc):
        dc.SetPen(wx.Pen('#d5d5d5'))
        alto = self.alto-50
        minimo = alto*0.1
        maximo = alto*0.9
        ancho = self.ancho-30
        dif = maximo - minimo
        for i in range(0,self.diven+1,1):
            dc.DrawLine(2, i*dif/self.diven+minimo, ancho, i*dif/self.diven+minimo)
        
        paso = int(round((ancho)/len(data)))
        if paso!=0:
            for i in range(int(round((ancho)/len(data))), ancho,paso):
                dc.DrawLine(i, 1, i, alto)
        
    def DrawTitle(self, dc):
        font =  dc.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.DrawText('Mediciones', (self.ancho-50)/2 ,self.alto-50)

    def DrawData(self, dc):
        dc.SetPen(wx.Pen('#0ab1ff'))
        alto = self.alto-50
        minimo = alto*0.1
        maximo = alto*0.9
        ancho = self.ancho-30
        dif = int(maximo - minimo)
        
        #acondicionamiento de los datos para la escala actual.
        if self.datos.dif!=0 and self.datos.size!=0:
            dataxy = [[(ancho)/self.datos.size*x,((float(y-self.datos.mini))/self.datos.dif)*dif+int(alto*0.1)-3,3,3] for x,y in enumerate(self.datos.data)]
        else:
            dataxy = [[(ancho)/self.datos.size*x,int(alto/2)+int(alto*0.1)-3,3,3] for x,y in enumerate(self.datos.data)]
        dc.SetPen(wx.Pen("RED", 5))
        dc.DrawEllipseList(dataxy)
        if self.datos.dif != 0:
            # Linea promedio.
            if self.padre.vermediamedida:
                dc.SetPen(wx.Pen("Green",2,wx.SHORT_DASH))
                dc.DrawLine(0,(self.datos.prom-self.datos.mini)/self.datos.dif*dif+int(alto*0.1)-3,ancho,(self.datos.prom-self.datos.mini)/self.datos.dif*dif+int(alto*0.1)-3)
                
                font =  wx.Font(8, wx.ROMAN,wx.NORMAL, wx.NORMAL)
                dc.SetFont(font)
                texto = u"Media = %.1f" % self.datos.prom
                dc.DrawText(texto,ancho-dc.GetTextExtent(texto)[0],(self.datos.prom-self.datos.mini)/self.datos.dif*dif+int(alto*0.1)-3),
            
            #lineas de desvío medio.
            if self.padre.verdesviomedido:
                dc.SetPen(wx.Pen("Gray",1,wx.SHORT_DASH))
                dc.DrawLine(0,(self.datos.prom-self.datos.mini+self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3\
                    ,ancho,(self.datos.prom-self.datos.mini+self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3)
                font =  wx.Font(8, wx.ROMAN, wx.NORMAL,wx.NORMAL)
                dc.SetFont(font)
                texto = u"Desvío = +/- %.1f" % self.datos.desmed
                dc.DrawText(texto,ancho-dc.GetTextExtent(texto)[0],(self.datos.prom-self.datos.mini+self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3)

                dc.DrawLine(0,(self.datos.prom-self.datos.mini-self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3,\
                    ancho,(self.datos.prom-self.datos.mini-self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3)
            #lineas de desvio y media indicadas por el usuario:
            #desvio calidad, media calidad:
            if self.padre.vermediacalidad:
                if self.padre.media:
                    dc.SetPen(wx.Pen("Blue",2,wx.SHORT_DASH))
                    dc.DrawLine(0,(self.padre.media-self.datos.mini)/self.datos.dif*dif+int(alto*0.1)-3,ancho,(self.padre.media-self.datos.mini)/self.datos.dif*dif+int(alto*0.1)-3)
                    font =  wx.Font(8, wx.ROMAN,wx.NORMAL, wx.NORMAL)
                    dc.SetFont(font)
                    texto = u"Media = %.1f" % self.padre.media
                    dc.DrawText(texto,0,(self.padre.media-self.datos.mini)/self.datos.dif*dif+int(alto*0.1)-3),
            if self.padre.verdesviocalidad:
                if self.padre.desvio and self.padre.media:
                    dc.SetPen(wx.Pen("Blue",1,wx.SHORT_DASH))
                    dc.DrawLine(0,(self.padre.media-self.datos.mini+self.padre.desvio)/self.datos.dif*dif+int(alto*0.1)-3\
                        ,ancho,(self.padre.media-self.datos.mini+self.padre.desvio)/self.datos.dif*dif+int(alto*0.1)-3)
                    font =  wx.Font(8, wx.ROMAN, wx.NORMAL,wx.NORMAL)
                    dc.SetFont(font)
                    texto = u"Desvío = +/- %.1f" % self.padre.desvio
                    dc.DrawText(texto,10+dc.GetTextExtent(texto)[0],(self.padre.media-self.datos.mini+self.padre.desvio)/self.datos.dif*dif+int(alto*0.1)-3)
        
                    dc.DrawLine(0,(self.padre.media-self.datos.mini-self.padre.desvio)/self.datos.dif*dif+int(alto*0.1)-3,\
                        ancho,(self.padre.media-self.datos.mini-self.padre.desvio)/self.datos.dif*dif+int(alto*0.1)-3)
                
            
                


class VerGrafico(wx.Frame):
    def __init__(self, parent, id, title,tabla=data):
        wx.Frame.__init__(self, parent, id, title, size=(900, 550))
        if tabla!=[]:
            #self.width,self.height = self.GetSize()
            self.tabla = [int(i[1]) for i in tabla]
            
            #----------------------------------------------------------#
            #flags para mostrar/ocutar lineas de media y desvios.
            #----------------------------------------------------------#
            self.vermediamedida = True
            self.vermediacalidad = False
            self.verdesviomedido = True
            self.verdesviocalidad = False
            #----------------------------------------------------------#
            #----------------------------------------------------------#
            #----------------------------------------------------------#
            self.media = None
            self.desvio = None
            
            self.linechart = LineChart(self,self.tabla)
            bSizer1 = wx.BoxSizer( wx.VERTICAL )
            bSizer1.Add( self.linechart, 1, wx.EXPAND |wx.ALL, 5 )
            
            bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
            
            gbSizer1 = wx.GridBagSizer( 0, 0 )
            gbSizer1.AddGrowableCol( 5 )
            gbSizer1.SetFlexibleDirection( wx.BOTH )
            gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
            
            self.cb_ValMedidos = wx.CheckBox( self, wx.ID_ANY, u"Ver Valores Medidos", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.cb_ValMedidos.SetValue(True) 
            gbSizer1.Add( self.cb_ValMedidos, wx.GBPosition( 0, 0 ), wx.GBSpan( 2, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
            
            self.cb_ValCalidad = wx.CheckBox( self, wx.ID_ANY, u"Ver Valores Calidad", wx.DefaultPosition, wx.DefaultSize, 0 )
            gbSizer1.Add( self.cb_ValCalidad, wx.GBPosition( 0, 3 ), wx.GBSpan( 2, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
            
            self.cb_mMedia = wx.CheckBox( self, wx.ID_ANY, u"Media", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.cb_mMedia.SetValue(True) 
            gbSizer1.Add( self.cb_mMedia, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.cb_mDesvio = wx.CheckBox( self, wx.ID_ANY, u"Desvío", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.cb_mDesvio.SetValue(True) 
            gbSizer1.Add( self.cb_mDesvio, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.cb_cMedia = wx.CheckBox( self, wx.ID_ANY, u"Media", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.cb_cMedia.Enable( False )
            
            gbSizer1.Add( self.cb_cMedia, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.cb_cDesvio = wx.CheckBox( self, wx.ID_ANY, u"Desvio", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.cb_cDesvio.Enable( False )
            
            gbSizer1.Add( self.cb_cDesvio, wx.GBPosition( 1, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
            gbSizer1.Add( self.m_staticline1, wx.GBPosition( 0, 2 ), wx.GBSpan( 4, 1 ), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
            
            self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Media:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText2.Wrap( -1 )
            gbSizer1.Add( self.m_staticText2, wx.GBPosition( 0, 6 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.tc_media = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
            gbSizer1.Add( self.tc_media, wx.GBPosition( 0, 7 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.btncargarmedia = wx.Button( self, wx.ID_ANY, u"Cargar", wx.DefaultPosition, wx.DefaultSize, 0 )
            gbSizer1.Add( self.btncargarmedia, wx.GBPosition( 0, 8 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Desvío", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText1.Wrap( -1 )
            gbSizer1.Add( self.m_staticText1, wx.GBPosition( 1, 6 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.tc_Desvio = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
            gbSizer1.Add( self.tc_Desvio, wx.GBPosition( 1, 7 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.btnCargarDesvio = wx.Button( self, wx.ID_ANY, u"Cargar", wx.DefaultPosition, wx.DefaultSize, 0 )
            gbSizer1.Add( self.btnCargarDesvio, wx.GBPosition( 1, 8 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
            
            bSizer2.Add( gbSizer1, 1, wx.EXPAND, 5 )
            
            bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )  
            
            self.SetSizer(bSizer1)
            
                    # Connect Events
            self.cb_ValMedidos.Bind( wx.EVT_CHECKBOX, self.OnVerValoresMedidos )
            self.cb_ValCalidad.Bind( wx.EVT_CHECKBOX, self.OnVerValoresCalidad )
            self.cb_mMedia.Bind( wx.EVT_CHECKBOX, self.OnMediaMedida )
            self.cb_mDesvio.Bind( wx.EVT_CHECKBOX, self.OnDesvioMedido )
            self.cb_cMedia.Bind( wx.EVT_CHECKBOX, self.OnMediaCalidad )
            self.cb_cDesvio.Bind( wx.EVT_CHECKBOX, self.OnDesvioCalidad )
            self.tc_media.Bind( wx.EVT_TEXT_ENTER, self.OnTextMedia )
            self.btncargarmedia.Bind( wx.EVT_BUTTON, self.OnTextMedia )
            self.tc_Desvio.Bind( wx.EVT_TEXT_ENTER, self.OnTextDesvio )
            self.btnCargarDesvio.Bind( wx.EVT_BUTTON, self.OnTextDesvio )
            self.tc_media.Bind(wx.EVT_CHAR, self.OnMediaChar)
            self.tc_Desvio.Bind(wx.EVT_CHAR, self.OnDesvioChar)
            self.Centre()
            self.Show(True)
        else:
            self.Destroy()
            
    def OnVerValoresMedidos( self, event ):
        if not self.cb_ValMedidos.GetValue():
            self.cb_mMedia.Enable( False )
            self.vermediamedida = False
            self.cb_mDesvio.Enable( False )
            self.verdesviomedido = False
        else:
            self.cb_mMedia.Enable( True )
            if self.cb_mMedia.GetValue():
                self.vermediamedida = True
            self.cb_mDesvio.Enable( True )
            if self.cb_mDesvio.GetValue():
                self.verdesviomedido = True
        self.linechart.OnSize(event)
            
        event.Skip()
    
    def OnVerValoresCalidad( self, event ):
        if not self.cb_ValCalidad.GetValue():
            self.cb_cMedia.Enable( False )
            self.vermediacalidad = False
            self.cb_cDesvio.Enable( False )
            self.verdesviocalidad = False
        else:
            self.cb_cMedia.Enable( True )
            if self.cb_cMedia.GetValue():
                self.vermediacalidad = True
            self.cb_cDesvio.Enable( True )
            if self.cb_cDesvio.GetValue():
                self.verdesviocalidad = True
        self.linechart.OnSize(event)
        event.Skip()
    
    def OnMediaMedida( self, event ):
        if self.cb_mMedia.GetValue():
            self.vermediamedida=True
        else:
            self.vermediamedida=False
        self.linechart.OnSize(event)
        event.Skip()
    
    def OnDesvioMedido( self, event ):
        if self.cb_mDesvio.GetValue():
            self.verdesviomedido=True
        else:
            self.verdesviomedido=False
        self.linechart.OnSize(event)
        event.Skip()
    
    def OnMediaCalidad( self, event ):
        if self.cb_cMedia.GetValue():
            self.vermediacalidad=True
        else:
            self.vermediacalidad=False
        self.linechart.OnSize(event)
        event.Skip()
    
    def OnDesvioCalidad( self, event ):
        if self.cb_cDesvio.GetValue():
            self.verdesviocalidad=True
        else:
            self.verdesviocalidad=False
        self.linechart.OnSize(event)
        event.Skip()
    
    def OnTextMedia( self, event ):
        self.media = float(self.tc_media.GetValue())
        self.linechart.OnSize(event)
        event.Skip()
        
    def OnTextDesvio( self, event ):
        self.desvio = float(self.tc_Desvio.GetValue())
        self.linechart.OnSize(event)
        event.Skip()
        
    def OnMediaChar( self, event ):
        if event.GetKeyCode() in [8,315,314,316,317]:
            event.Skip()
            return
        caracter = chr(event.GetUniChar())
        if caracter in ["1","2","3","4","5","6","7","8","9","0","."]:
            event.Skip()
        else:
            return
    def OnDesvioChar(self,event):        
        if event.GetKeyCode() in [8,315,314,316,317]:
            event.Skip()
            return
        caracter = chr(event.GetUniChar())
        if caracter in ["1","2","3","4","5","6","7","8","9","0",","]:
            event.Skip()
        else:
            return

if __name__ == '__main__':
    app = wx.App(0)
    VerGrafico(None, -1, 'Valores Medidos')
    app.MainLoop()
