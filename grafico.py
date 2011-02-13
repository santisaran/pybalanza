#!/usr/bin/python
# -*- coding: utf-8 -*-
# linechart.py
import time
import wx
import random
data = [random.randint(950,1050) for i in range(20)]

#muestras = ('10', '20', '30')
class prosdata():
    def __init__(self,datos):
        self.data=datos
        
        #valor máximo
        self.maxim = max(datos)
        #valor minimo
        self.mini = min(datos)
        #tamaño cuantas piezas fueron pesadas
        self.size = len(datos)
        #diferencia entre minima y máxima para autoescalar el gráfico
        self.dif = self.maxim-self.mini
        #promedio 
        self.prom = float(sum(self.data))/len(self.data)
        #desvío medio.
        self.desmed = float(sum([abs(i-self.prom) for i in self.data]))/self.size
        
class LineChart(wx.Window): 
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.SetBackgroundColour('WHITE')
        self.datos = prosdata(data)
        self.InitBuffer()        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)



    def OnSize(self, evt):
        # When the window size changes we need a new buffer.
        self.InitBuffer()
        
    def InitBuffer(self):
        # Create the buffer bitmap to be the same size as the window,
        # then draw our graph to it.  Since we use wx.BufferedDC
        # whatever is drawn to the buffer is also drawn to the window.
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
    
    def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self, self.buffer)


    def DrawAxis(self, dc):
        dc.SetPen(wx.Pen('#0AB1FF'))
        font =  dc.GetFont()
        font.SetPointSize(8)
        dc.SetFont(font)
        dc.DrawLine(1, 1, self.ancho-30, 1)
        dc.DrawLine(1, 1, 1, self.alto-20)
        alto = self.alto-50
        minimo = alto*0.1
        maximo = alto*0.9
        ancho = self.ancho-30
        dif = maximo - minimo
        self.coordmin = int(dif/self.datos.dif*self.datos.mini) #valor minimo en el grafico.
        self.coordmax = int(dif/self.datos.dif*self.datos.maxim) #valor maximo en el gráfico.
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

        for i in range(int(round(ancho/len(data)))+1, ancho,int(round(ancho/len(data)))):
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
        dataxy = [[(ancho)/self.datos.size*x,((float(y-self.datos.mini))/self.datos.dif)*dif+int(alto*0.1)-3,6,6] for x,y in enumerate(self.datos.data)]
        dc.SetPen(wx.Pen("blue", 2,wx.STIPPLE))
        dc.DrawEllipseList(dataxy)
        
        # Linea promedio.
        dc.SetPen(wx.Pen("Green",2,wx.SHORT_DASH))
        dc.DrawLine(0,(self.datos.prom-self.datos.mini)/self.datos.dif*dif+int(alto*0.1)-3,ancho,(self.datos.prom-self.datos.mini)/self.datos.dif*dif+int(alto*0.1)-3)

        dc.SetPen(wx.Pen("LightGray",1,wx.SHORT_DASH))
        dc.DrawLine(0,(self.datos.prom-self.datos.mini+self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3\
            ,ancho,(self.datos.prom-self.datos.mini+self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3)
        dc.DrawLine(0,(self.datos.prom-self.datos.mini-self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3,\
            ancho,(self.datos.prom-self.datos.mini-self.datos.desmed)/self.datos.dif*dif+int(alto*0.1)-3)


class LineChartExample(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 300))
        self.width,self.height = self.GetSize()
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('WHITE')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        linechart = LineChart(panel)
        hbox.Add(linechart, 1, wx.EXPAND | wx.ALL, 15)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

if __name__ == '__main__':
    app = wx.App(0)
    LineChartExample(None, -1, 'Valores Medidos')
    app.MainLoop()
