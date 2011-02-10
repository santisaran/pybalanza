#!/usr/bin/python

# linechart.py

import wx

data = [7,8,11,3,12,30,6,6,10,78,65,77]

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
        self.ancho,self.alto = self.GetSize()
        dc.SetDeviceOrigin(30, self.alto-30)
        dc.SetAxisOrientation(True, True)
        dc.SetPen(wx.Pen('WHITE'))
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
        ancho = self.ancho-30
        for i in range(int(min(data)*0.9),int(round(max(data)*1.1)),self.datos.dif/8):
            i_ = alto/int(round(max(data)*1.1))*i
            dc.DrawText(str(i), -30, i_)
            dc.DrawLine(2,i_, -5,i_)

        for i in range(0, 300,int(round(ancho/len(data)))):
            dc.DrawLine(i, 2, i, -5)
        
        self.datos.size 
        
        for i in range(0,self.datos.size,self.datos.size/5):
            dc.DrawText(str(i),ancho/self.datos.size*i-10,-10)

    def DrawGrid(self, dc):
        dc.SetPen(wx.Pen('#d5d5d5'))

        for i in range(20, 220, 20):
            dc.DrawLine(2, i, 300, i)

        for i in range(100, 300, 100):
            dc.DrawLine(i, 2, i, 200)

    def DrawTitle(self, dc):
        font =  dc.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.DrawText('Mediciones', 90, 235)


    def DrawData(self, dc):
        dc.SetPen(wx.Pen('#0ab1ff'))
        dataxy = [[300/len(data)*x,10*y] for x,y in enumerate(data)]
        print dataxy
        for i in range(10, 310, 10):
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
