#!/usr/bin/python
# -*- coding: utf-8 -*-
# linechart.py
import time
import wx

data = [10,20,36,25,10,34,24]

#muestras = ('10', '20', '30')
class prosdata():
    def __init__(self,datos):
        self.data=datos
        self.maxim = max(datos)
        self.mini = min(datos)
        self.size = len(datos)
        self.dif = self.maxim-self.mini
        self.prom = float(sum(self.data))/len(self.data)
        
class LineChart(wx.Panel): 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('WHITE')
        self.datos = prosdata(data)
        print self.datos.maxim
        print self.datos.mini
        print self.datos.size
        print self.datos.dif
        print self.datos.prom
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        self.ancho,self.alto = self.GetSize()
        print self.ancho,self.alto
        dc.SetDeviceOrigin(30, self.alto-30)
        dc.SetAxisOrientation(True, True)
        dc.SetPen(wx.Pen('WHITE'))
        dc.SetBrush(wx.Brush('GREEN',wx.SOLID))
        dc.DrawRectangle(1, 1, self.alto-10, self.ancho-10)
        self.DrawAxis(dc)
        self.DrawGrid(dc)
        self.DrawTitle(dc)
        self.DrawData(dc)

    def DrawAxis(self, dc):
        dc.SetPen(wx.Pen('#0AB1FF'))
        font =  dc.GetFont()
        font.SetPointSize(8)
        dc.SetFont(font)
        dc.DrawLine(1, 1, self.ancho-30, 1)
        dc.DrawLine(1, 1, 1, self.alto-50)
        alto = self.alto-50
        minimo = alto*0.1

        maximo = alto*0.9

        ancho = self.ancho-30
        dif = maximo - minimo
        coordmin = int(dif/self.datos.dif*self.datos.mini) #valor minimo en el grafico.
        coordmax = int(dif/self.datos.dif*self.datos.maxim) #valor maximo en el gráfico.
        diven = 4
        for i in range(0,diven+1,1):
            dc.DrawText("%.2f"%(float(i*self.datos.dif)/diven+self.datos.mini), -30, i*dif/diven+minimo+5)
            dc.DrawLine(4,i*dif/diven+minimo, -5,i*dif/diven+minimo)
            
        for i in range(1, ancho,int(round(ancho/len(data)))):
            dc.DrawLine(i, 2, i, -5)
        
        self.datos.size 
        
        for i in range(0,self.datos.size,self.datos.size/5 if self.datos.size/5>=1 else 1):
            dc.DrawText(str(i),ancho/self.datos.size*i-10,-10)

    def DrawGrid(self, dc):
        dc.SetPen(wx.Pen('#d5d5d5'))
        alto = self.alto-50
        minimo = alto*0.1
        maximo = alto*0.9
        ancho = self.ancho-30
        dif = maximo - minimo
        for i in range(int(min(data)*0.9),int(round(max(data)*1.1)),self.datos.dif/8 if self.datos.dif/8>=1 else 1):
            i_ = alto/int(round(max(data)*1.1))*i
            dc.DrawLine(2, i_, ancho, i_)

        for i in range(100, 300, 100):
            dc.DrawLine(i, 2, i, 200)

    def DrawTitle(self, dc):
        font =  dc.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.DrawText('Mediciones', 90, 235)


    def DrawData(self, dc):
        dc.SetPen(wx.Pen('#0ab1ff'))
        alto = self.alto-50
        minimo = alto*0.1
        maximo = alto*0.9
        ancho = self.ancho-30
        dif = maximo - minimo
        dataxy = [[(self.ancho-30)/self.datos.size*x,(y-self.datos.mini)/self.datos.dif*dif+20] for x,y in enumerate(data)]
        print dataxy
        #for i in range(0, self.datos.size, 10):
        dc.DrawSpline(dataxy)


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
    app = wx.App()
    LineChartExample(None, -1, 'Valores Medidos')
    app.MainLoop()
